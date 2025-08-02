#include <chrono>
#include <cstdio>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>
#include <fstream>
#include <glob.h>      // 用于文件模式匹配
#include <vector>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float32.hpp"
#include "std_msgs/msg/bool.hpp"

using namespace std::chrono_literals;

#define DEVICE_NAME "/dev/i2c-4"
#define DEVICE_ADDR 0x38

class SensorNode : public rclcpp::Node
{
public:
    SensorNode() : Node("sensor_node")
    {
        temperature_publisher_ = this->create_publisher<std_msgs::msg::Float32>("temp", 10);
        humidity_publisher_    = this->create_publisher<std_msgs::msg::Float32>("hum", 10);
        mq2_publisher_         = this->create_publisher<std_msgs::msg::Bool>("mq2", 10);
        cpuT_publisher_     = this->create_publisher<std_msgs::msg::Float32>("cpuT", 10);
        npu_publisher_     = this->create_publisher<std_msgs::msg::Float32>("npu", 10);

        init_sensor();

        led_subscriber_ = this->create_subscription<std_msgs::msg::Bool>(
            "led", 10,
            std::bind(&SensorNode::led_callback, this, std::placeholders::_1));

        init_mq2();

        // 等待 100ms 确保文件系统设备准备完毕
        usleep(100000);

        // 每 200ms 读取并发布所有数据
        timer_ = this->create_wall_timer(50ms, std::bind(&SensorNode::read_and_publish, this));
    }

private:
    // I2C 相关
    int fd_;

    // GPIO 读取缓存
    std::string gpio_value_;

    // 发布者
    rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr temperature_publisher_;
    rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr humidity_publisher_;
    rclcpp::Publisher<std_msgs::msg::Bool>::SharedPtr    mq2_publisher_;
    rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr npu_publisher_;
    rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr cpuT_publisher_;

    //订阅者
    rclcpp::Subscription<std_msgs::msg::Bool>::SharedPtr led_subscriber_;

    rclcpp::TimerBase::SharedPtr                         timer_;

    float humidity;
    float temperature;
    bool gpio101_state_ = false;
    bool gpio97_state_ = false;

    void led_callback(const std_msgs::msg::Bool::SharedPtr msg)
    {
        gpio101_state_ = msg->data;
        write_gpio101(gpio101_state_);
        // RCLCPP_INFO(this->get_logger(), "Set LED: %s", gpio101_state_ ? "ON" : "OFF");
    }

    void init_sensor()
    {
        fd_ = open(DEVICE_NAME, O_RDWR);
        if (fd_ < 0) {
            RCLCPP_ERROR(this->get_logger(), "Failed to open I2C device %s", DEVICE_NAME);
            rclcpp::shutdown();
            return;
        }
        if (ioctl(fd_, I2C_SLAVE_FORCE, DEVICE_ADDR) < 0) {
            RCLCPP_ERROR(this->get_logger(), "Failed to set I2C address 0x%X", DEVICE_ADDR);
            rclcpp::shutdown();
            return;
        }

        unsigned char wr_buf[3] = {0xE1, 0x08, 0x00};
        write(fd_, wr_buf, 3);
        sleep(1);
    }

    void init_mq2()
    {
        // system("echo 109 > /sys/class/gpio/export");
        // system("echo in  > /sys/class/gpio/gpio109/direction");
    }

    void read_gpio()
    {
        std::ifstream gpio_file("/sys/class/gpio/gpio109/value");
        if (gpio_file.is_open()) {
            gpio_file >> gpio_value_;
        } else {
            RCLCPP_ERROR(this->get_logger(), "Failed to read GPIO value");
        }
    }

    void write_gpio101(bool value)
    {
        std::ofstream gpio_file("/sys/class/gpio/gpio101/value");
        if (gpio_file.is_open()) {
            gpio_file << (value ? "1" : "0");
        } else {
            RCLCPP_ERROR(this->get_logger(), "Failed to write GPIO101");
        }
    }

    void write_gpio97(bool value)
    {
        std::ofstream gpio_file("/sys/class/gpio/gpio97/value");
        if (gpio_file.is_open()) {
            gpio_file << (value ? "1" : "0");
        } else {
            RCLCPP_ERROR(this->get_logger(), "Failed to write GPIO101");
        }
    }

    /// 读取所有 thermal_zone*/temp 的平均值（摄氏度）
    float read_cpu_temp()
    {
        glob_t glob_result;
        std::vector<float> temps;
        // 匹配所有 thermal_zone*/temp
        if (glob("/sys/class/thermal/thermal_zone*/temp", 0, nullptr, &glob_result) == 0) {
            for (size_t i = 0; i < glob_result.gl_pathc; ++i) {
                std::ifstream ifs(glob_result.gl_pathv[i]);
                if (ifs.is_open()) {
                    int milli;
                    ifs >> milli;
                    temps.push_back(static_cast<float>(milli) / 1000.0f);
                }
            }
        }
        globfree(&glob_result);

        if (temps.empty()) {
            return -1.0f;  // 读取失败
        }
        float sum = 0.0f;
        for (auto t : temps) sum += t;
        return sum / temps.size();
    }

    //NPU
    float read_npu_status()
    {
        std::ifstream load_file("/home/uboot/data/npu_status.txt");
        std::ifstream freq_file("/sys/class/devfreq/fdab0000.npu/cur_freq");

        if (!load_file.is_open() || !freq_file.is_open()) {
            return -1.0f;
        }

        std::string time, line;
        std::getline(load_file, time);
        std::getline(load_file, line);  // 读取整行，如 "NPU load:  Core0: 38%, Core1:  0%, Core2:  0%,"
        

        int core0 = -1, core1 = -1, core2 = -1;
        sscanf(line.c_str(), "NPU load:  Core0: %d%%, Core1: %d%%, Core2: %d%%,", &core0, &core1, &core2);

        int freq = -1;
        freq_file >> freq;

        if (core0 < 0 || core1 < 0 || core2 < 0 || freq < 0) {
            return -1.0f;
        }

        float avg_load = (core0 + core1 + core2) / 3.0f;

        // 如果你希望加入频率因子（可选）
        // float freq_ghz = freq / 1e9f;
        // return avg_load * freq_ghz / 100.0f;

        return avg_load;
    }

    void read_and_publish()
    {
        // —— I2C 传感器读取 —— //
        unsigned char wr_buf[3] = {0xAC, 0x33, 0x00};
        unsigned char rd_buf[6] = {0};
        write(fd_, wr_buf, 3);
        // usleep(100000);
        int ret = read(fd_, rd_buf, 6);
        if (ret != 6) {
            RCLCPP_WARN(this->get_logger(), "I2C read failed");
        } else {
            int h1 = (rd_buf[1] << 12) | (rd_buf[2] << 4) | (rd_buf[3] >> 4);
            int t1 = ((rd_buf[3] & 0x0F) << 16) | (rd_buf[4] << 8) | rd_buf[5];
            humidity    = h1 * 100.0f   / 1048576.0f;
            temperature = t1 * 200.0f   / 1048576.0f - 50.0f;

            std_msgs::msg::Float32 temp_msg, hum_msg;
            temp_msg.data = temperature;
            hum_msg.data  = humidity;
            temperature_publisher_->publish(temp_msg);
            humidity_publisher_->publish(hum_msg);
        }

        // —— MQ2 GPIO 读取 —— //
        read_gpio();
        std_msgs::msg::Bool mq2_msg;
        mq2_msg.data = (gpio_value_ == "0");
        mq2_publisher_->publish(mq2_msg);

        //GOIO 
        // gpio97_state_ = !gpio97_state_;
        // write_gpio97(gpio97_state_);

        // —— CPU 温度读取 & 发布 —— //
        float cpu_temp = read_cpu_temp();
        std_msgs::msg::Float32 cpu_msg;
        cpu_msg.data = cpu_temp;
        cpuT_publisher_->publish(cpu_msg);

        // —— NPU 占用率读取 & 发布 —— //
        float npu_score = read_npu_status();
        std_msgs::msg::Float32 npu_msg;
        npu_msg.data = npu_score;
        npu_publisher_->publish(npu_msg);

        // // 日志输出
        // RCLCPP_INFO(this->get_logger(),
        //     "Temp: %.2f °C, Humidity: %.2f %%, MQ2: %s, CPU Temp: %.2f °C, NPU: %.2f%%",
        //     temperature, // 占位，不打印订阅数
        //     humidity,
        //     mq2_msg.data ? "TRUE" : "FALSE",
        //     cpu_temp,
        //     npu_score
        // );
    }
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<SensorNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
