#include "rclcpp/rclcpp.hpp"
#include "std_srvs/srv/trigger.hpp"

#include <fstream>
#include <string>
#include <chrono>
#include <unistd.h>
#include <cstdlib>

#define GPIO_NUM 107
#define GPIO_PATH "/sys/class/gpio/"
#define GPIO_VALUE_PATH "/sys/class/gpio/gpio107/value"
#define GPIO_DIRECTION_PATH "/sys/class/gpio/gpio107/direction"

using namespace std::chrono_literals;

class HumanDetectorClient : public rclcpp::Node
{
public:
    HumanDetectorClient() : Node("human_detector_client")
    {
        client_ = this->create_client<std_srvs::srv::Trigger>("do_something");
        setup_gpio();
        timer_ = this->create_wall_timer(200ms, std::bind(&HumanDetectorClient::check_gpio, this));
        RCLCPP_INFO(this->get_logger(), "人体检测客户端启动，等待有人触发...");
    }

private:
    rclcpp::Client<std_srvs::srv::Trigger>::SharedPtr client_;
    rclcpp::TimerBase::SharedPtr timer_;
    std::string last_state_ = "0";

    void setup_gpio()
    {
        std::string gpio_dir = std::string(GPIO_PATH) + "gpio" + std::to_string(GPIO_NUM);
        if (access(gpio_dir.c_str(), F_OK) == -1)
        {
            std::string export_cmd = "echo " + std::to_string(GPIO_NUM) + " > " + GPIO_PATH + "export";
            system(export_cmd.c_str());
            usleep(10000);
        }

        std::ofstream dir_file(GPIO_DIRECTION_PATH);
        if (dir_file.is_open())
        {
            dir_file << "in";
            dir_file.close();
        }
    }

    void check_gpio()
    {
        std::ifstream gpio_file(GPIO_VALUE_PATH);
        std::string value;

        if (gpio_file.is_open())
        {
            std::getline(gpio_file, value);
            gpio_file.close();

            // 上升沿检测（0 -> 1）
            if (value == "1" && last_state_ == "0")
            {
                RCLCPP_INFO(this->get_logger(), "检测到人体！正请求服务...");
                if (!client_->wait_for_service(1s))
                {
                    RCLCPP_WARN(this->get_logger(), "服务未就绪");
                    return;
                }

                auto request = std::make_shared<std_srvs::srv::Trigger::Request>();
                client_->async_send_request(request);
                last_state_ = "1";

                // 防抖
                std::this_thread::sleep_for(std::chrono::seconds(5));
            }
            else if (value == "0")
            {
                last_state_ = "0";
            }
        }
    }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<HumanDetectorClient>());
    rclcpp::shutdown();
    return 0;
}
