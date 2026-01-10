import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool
from geometry_msgs.msg import Twist
from time import time


class ledControl(Node):
    def __init__(self):
        super().__init__('ledControl_server')
        self.led_publisher = self.create_publisher(Bool, '/led', 10)
        self.switch = Bool()
        self.turn_on()

    def turn_on(self):
        self.switch.data = True
        self.led_publisher.publish(self.switch)

    def turn_off(self):
        self.switch.data = False
        self.led_publisher.publish(self.switch)

    def toggle(self):
        self.switch.data = not self.switch.data
        self.led_publisher.publish(self.switch)


class ledStateMachine(ledControl):
    def __init__(self):
        super().__init__()
        self.subscription_nav = self.create_subscription(Twist, '/cmd_vel', self.nav_callback, 10)
        self.subscription_yolo = self.create_subscription(String, '/yolo/detect_info', self.yolo_callback, 10)
        self.timer_check = self.create_timer(0.01, self.timer_check_callback)
        self.state = 0  # 0 正常态; 1 导航态; 2 识别态
        self.msg_time = time()  # 上一次接受到消息的时间
        self.last_control_time = time()  # 上一次转变灯的开关的时间

    def turn_into_state_n(self, n):
        if n in [0, 1, 2, -1]:
            self.state = n

    def nav_callback(self, msg):
        self.msg_time = time()
        self.turn_into_state_n(1)

    def yolo_callback(self, msg):
        self.msg_time = time()
        if self.state != 1:
            self.turn_into_state_n(2)

    def timer_check_callback(self):
        if (time() - self.msg_time) > 0.5:
            self.turn_into_state_n(0)
        if self.state == 0:
            self.turn_on()
        elif self.state == 1:
            if (time() - self.last_control_time) > 0.1:
                self.toggle()
                self.last_control_time = time()
        elif self.state == 2:
            if (time() - self.last_control_time) > 0.3:
                self.toggle()
                self.last_control_time = time()
        elif self.state == -1:
            self.turn_off()

    def end(self):
        self.turn_into_state_n(-1)
        self.turn_off()


def main():
    rclpy.init()
    led_node = ledStateMachine()
    try:
        rclpy.spin(led_node)  # 启动节点的事件循环
    except KeyboardInterrupt:
        led_node.end()
        led_node.destroy_node()  # 清理并关闭节点
    finally:
        rclpy.shutdown()  # 关闭ROS2


if __name__ == '__main__':
    main()