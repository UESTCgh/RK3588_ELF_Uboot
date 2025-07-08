#include "rclcpp/rclcpp.hpp"
#include "std_srvs/srv/trigger.hpp"

class DoSomethingServer : public rclcpp::Node
{
public:
    DoSomethingServer() : Node("do_something_server")
    {
        service_ = this->create_service<std_srvs::srv::Trigger>(
            "do_something",
            std::bind(&DoSomethingServer::handle_request, this, std::placeholders::_1, std::placeholders::_2)
        );

        RCLCPP_INFO(this->get_logger(), "服务已启动：/do_something");
    }

private:
    rclcpp::Service<std_srvs::srv::Trigger>::SharedPtr service_;

    void handle_request(
        const std::shared_ptr<std_srvs::srv::Trigger::Request> request,
        std::shared_ptr<std_srvs::srv::Trigger::Response> response)
    {
        (void)request;
        RCLCPP_INFO(this->get_logger(), "收到检测请求，执行操作");
        
        // 这里写你要做的事，比如开灯、拍照、调用API等
        // system("echo '[人体检测] 执行了动作' >> /tmp/human.log");

        response->success = true;
        response->message = "已执行动作";
    }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<DoSomethingServer>());
    rclcpp::shutdown();
    return 0;
}
