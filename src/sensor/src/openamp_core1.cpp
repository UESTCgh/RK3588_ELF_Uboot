#include "rclcpp/rclcpp.hpp"
#include "sensor/msg/device_status.hpp"
#include "sensor/msg/core_command.hpp"

#include <fcntl.h>
#include <unistd.h>
#include <poll.h>
#include <sys/ioctl.h>
#include <linux/rpmsg.h>
#include <cstring>
#include <cstdio>
#include <cerrno>

#define MAX_DATA_LENGTH 256

#define DEVICE_CORE_START 0x0001U
#define DEVICE_CORE_STOP  0x0002U
#define DEVICE_CORE_CHECK 0x0003U

struct DeviceStatusRaw {
    int led = 1;
    int pwm = 6;
    float temperature = -1;
    float humidity = -1;
    int presence = -1;
    int mq2 = -1;
    int val = -1;
};

struct DataPacket {
    uint32_t command;
    uint16_t length;
    char data[MAX_DATA_LENGTH];
};

DeviceStatusRaw device;

ssize_t write_full(int fd, void *buf, size_t count) {
    ssize_t total = 0;
    while (count) {
        ssize_t ret = write(fd, buf, count);
        if (ret < 0) {
            if (errno == EINTR) continue;
            return -1;
        }
        count -= ret;
        buf = static_cast<char*>(buf) + ret;
        total += ret;
    }
    return total;
}

ssize_t read_full(int fd, void *buf, size_t count) {
    ssize_t res;
    do {
        res = read(fd, buf, count);
    } while (res < 0 && errno == EINTR);
    if (res < 0 && errno == EAGAIN) return 0;
    if (res < 0) return -1;
    return res;
}

class OpenAMPNode : public rclcpp::Node {
public:
    OpenAMPNode() : Node("openamp_core1") {
        status_pub_ = this->create_publisher<sensor::msg::DeviceStatus>("from_core", 10);
        command_sub_ = this->create_subscription<sensor::msg::CoreCommand>(
            "to_core", 10, std::bind(&OpenAMPNode::command_callback, this, std::placeholders::_1));

        init_rpmsg();
        timer_ = this->create_wall_timer(std::chrono::milliseconds(1000), std::bind(&OpenAMPNode::loop, this));
    }

    ~OpenAMPNode() {
        if (rpmsg_fd_ >= 0) close(rpmsg_fd_);
        if (ctrl_fd_ >= 0) close(ctrl_fd_);
    }

private:
    void command_callback(const sensor::msg::CoreCommand::SharedPtr msg) {
        device.led = msg->led;
        device.pwm = msg->pwm;
    }

    void init_rpmsg() {
        ctrl_fd_ = open("/dev/rpmsg_ctrl0", O_RDWR);
        if (ctrl_fd_ < 0) {
            RCLCPP_ERROR(this->get_logger(), "Failed to open rpmsg_ctrl0");
            return;
        }

        struct rpmsg_endpoint_info eptinfo = {};
        strncpy(eptinfo.name, "xxxx", sizeof(eptinfo.name));
        eptinfo.src = 0;
        eptinfo.dst = 0;

        if (ioctl(ctrl_fd_, RPMSG_CREATE_EPT_IOCTL, &eptinfo)) {
            RCLCPP_ERROR(this->get_logger(), "Failed to create RPMsg endpoint");
            close(ctrl_fd_);
            ctrl_fd_ = -1;
            return;
        }

        rpmsg_fd_ = open("/dev/rpmsg0", O_RDWR);
        if (rpmsg_fd_ < 0) {
            RCLCPP_ERROR(this->get_logger(), "Failed to open rpmsg0");
            close(ctrl_fd_);
            ctrl_fd_ = -1;
        }
    }

    void loop() {
        if (rpmsg_fd_ < 0) return;
    
        DataPacket send_pkt, recv_pkt;
        char recv_buff[MAX_DATA_LENGTH];
    
        int len = snprintf(send_pkt.data, MAX_DATA_LENGTH, "LED:%1d|PWM:%03d", device.led, device.pwm);
        send_pkt.command = DEVICE_CORE_CHECK;
        send_pkt.length = static_cast<uint16_t>(len);
    
        RCLCPP_INFO(this->get_logger(), "Sending: %s", send_pkt.data);
        write_full(rpmsg_fd_, &send_pkt, sizeof(DataPacket));
    
        struct pollfd fds = { rpmsg_fd_, POLLIN, 0 };
        if (poll(&fds, 1, 100) > 0 && (fds.revents & POLLIN)) {
            if (read_full(rpmsg_fd_, &recv_pkt, sizeof(DataPacket)) > 0) {
                std::memcpy(recv_buff, recv_pkt.data, recv_pkt.length);
                recv_buff[recv_pkt.length] = '\0';
    
                RCLCPP_INFO(this->get_logger(), "Received raw: %s", recv_buff);
    
                if (recv_pkt.length >= 25 &&
                    sscanf(recv_pkt.data, "T:%f|H:%f|P:%d|M:%d|V:%d",
                        &device.temperature, &device.humidity,
                        &device.presence, &device.mq2, &device.val) == 5) {
    
                    // Validate
                    if (device.temperature < 0 || device.temperature > 100) device.temperature = -1;
                    if (device.humidity < 0 || device.humidity > 100) device.humidity = -1;
                    if (device.presence != 0 && device.presence != 1) device.presence = -1;
                    if (device.mq2 != 0 && device.mq2 != 1) device.mq2 = -1;
                    if (device.val != 0 && device.val != 1) device.val = -1;
                }
    
                auto msg = sensor::msg::DeviceStatus();
                msg.temperature = device.temperature;
                msg.humidity = device.humidity;
                msg.presence = device.presence;
                msg.mq2 = device.mq2;
                msg.val = device.val;
    
                RCLCPP_INFO(this->get_logger(), "Published: T=%.1f H=%.1f P=%d M=%d V=%d",
                            msg.temperature, msg.humidity, msg.presence, msg.mq2, msg.val);
    
                status_pub_->publish(msg);
            } else {
                RCLCPP_WARN(this->get_logger(), "Failed to read from rpmsg");
            }
        } else {
            RCLCPP_DEBUG(this->get_logger(), "No data from rpmsg this cycle");
        }
    }
    
    rclcpp::Publisher<sensor::msg::DeviceStatus>::SharedPtr status_pub_;
    rclcpp::Subscription<sensor::msg::CoreCommand>::SharedPtr command_sub_;
    rclcpp::TimerBase::SharedPtr timer_;
    int ctrl_fd_ = -1;
    int rpmsg_fd_ = -1;
};
  
int main(int argc, char *argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<OpenAMPNode>());
    rclcpp::shutdown();
    return 0;
}
