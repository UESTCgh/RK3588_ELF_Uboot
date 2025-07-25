#include <chrono>
#include <cstdio>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>
#include <fstream>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float32.hpp"
#include "std_msgs/msg/bool.hpp"  // 加入 Bool 类型支持

using namespace std::chrono_literals;

#define DEVICE_NAME "/dev/i2c-4"
#define DEVICE_ADDR 0x38

class SensorNode : public rclcpp::Node
{
public:
    SensorNode() : Node("sensor_node")
    {
        temperature_publisher_ = this->create_publisher<std_msgs::msg::Float32>("temperature", 10);
        humidity_publisher_ = this->create_publisher<std_msgs::msg::Float32>("humidity", 10);
        mq2_publisher_ = this->create_publisher<std_msgs::msg::Bool>("mq2", 10);
        init_sensor();
        init_mq2();
        usleep(100000);  // 等待100ms确保文件系统生成
        timer_ = this->create_wall_timer(500ms, std::bind(&SensorNode::read_and_publish, this));
    }

private:
    rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr temperature_publisher_;
    rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr humidity_publisher_;
    rclcpp::Publisher<std_msgs::msg::Bool>::SharedPtr mq2_publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
    int fd_;
    std::string gpio_value_;  // GPIO值为字符串形式读取

    void init_sensor()
    {
        fd_ = open(DEVICE_NAME, O_RDWR);
        if (fd_ < 0)
        {
            RCLCPP_ERROR(this->get_logger(), "Failed to open I2C device");
            rclcpp::shutdown();
            return;
        }

        if (ioctl(fd_, I2C_SLAVE_FORCE, DEVICE_ADDR) < 0)
        {
            RCLCPP_ERROR(this->get_logger(), "Failed to set I2C address");
            rclcpp::shutdown();
            return;
        }

        unsigned char wr_buf[3] = {0xe1, 0x08, 0x00};
        write(fd_, wr_buf, 3);
        sleep(1);
    }

    void init_mq2()
    {
        // Export the GPIO pin
        system("echo 449 > /sys/class/gpio/export");

        // Set GPIO pin as input
        system("echo in > /sys/class/gpio/gpio449/direction");
    }

    void read_gpio()
    {
        // Read the value of GPIO pin
        std::ifstream gpio_file("/sys/class/gpio/gpio449/value");
        if (gpio_file.is_open())
        {
            gpio_file >> gpio_value_;
        }
        else
        {
            RCLCPP_ERROR(this->get_logger(), "Failed to read GPIO value");
        }
    }

    void read_and_publish()
    {
        unsigned char wr_buf[3] = {0xac, 0x33, 0x00};
        unsigned char rd_buf[6] = {0};

        write(fd_, wr_buf, 3);
        // sleep(1);
        usleep(100000);//100ms
        int ret = read(fd_, rd_buf, 6);
        if (ret != 6)
        {
            RCLCPP_WARN(this->get_logger(), "I2C read failed");
            return;
        }

        int h1 = (rd_buf[1] << 12) | (rd_buf[2] << 4) | (rd_buf[3] >> 4);
        int t1 = ((rd_buf[3] & 0x0F) << 16) | (rd_buf[4] << 8) | rd_buf[5];

        float humidity = h1 * 100.0 / 1048576.0;
        float temperature = t1 * 200.0 / 1048576.0 - 50;

        std_msgs::msg::Float32 temp_msg;
        std_msgs::msg::Float32 hum_msg;
        temp_msg.data = temperature;
        hum_msg.data = humidity;

        temperature_publisher_->publish(temp_msg);
        humidity_publisher_->publish(hum_msg);

        // RCLCPP_INFO(this->get_logger(), "Temp: %.2f °C, Humidity: %.2f %%", temperature, humidity);

        // Read the GPIO value

        read_gpio();
        std_msgs::msg::Bool mq2_msg;
        mq2_msg.data = (gpio_value_ == "0");  // Convert "1" or "0"
        mq2_publisher_->publish(mq2_msg);

        RCLCPP_INFO(this->get_logger(), "Temp: %.2f °C, Humidity: %.2f %% MQ2: %s", temperature, humidity, mq2_msg.data ? "TRUE" : "FALSE");
    }
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<SensorNode>());
    rclcpp::shutdown();
    return 0;
}
