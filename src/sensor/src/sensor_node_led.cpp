#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/bool.hpp>
#include <fstream>

class SensorNode : public rclcpp::Node
{
public:
    SensorNode() : Node("sensor_node")
    {
        // 订阅 /led1
        led_subscriber_ = this->create_subscription<std_msgs::msg::Bool>(
            "led1", 10,
            std::bind(&SensorNode::led_callback, this, std::placeholders::_1));

    }

private:
    rclcpp::Subscription<std_msgs::msg::Bool>::SharedPtr led_subscriber_;

    void led_callback(const std_msgs::msg::Bool::SharedPtr msg)
    {
        write_gpio101(msg->data);
        RCLCPP_INFO(this->get_logger(), "Set LED1: %s", msg->data ? "ON" : "OFF");
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
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<SensorNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}