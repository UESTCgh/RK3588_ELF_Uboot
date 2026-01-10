import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool, UInt16
from sensor_msgs.msg import LaserScan
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


class BreathingLightNode(ledStateMachine):
    def __init__(self):
        super().__init__()
        
        # 订阅两个话题
        self.sub_scan = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.sub_mq2 = self.create_subscription(Bool, '/mq2', self.mq2_callback, 10)
        
        # 发布 PWM
        self.pub_pwm = self.create_publisher(UInt16, '/pwm', 10)

        # 状态
        self.scan_received = False  
        self.last_scan_time = 0.0   # 最近一次收到 /scan 消息的时间
        self.scan_timeout = 0.2     # 100ms 超时
        self.mq2_active = False     
        
        # 呼吸灯参数
        self.pwm_value = 1
        self.direction = 1  # 1: 增亮, -1: 变暗

        # 定时器（循环控制呼吸灯）
        self.timer = self.create_timer(0.01, self.timer_callback)


    def scan_callback(self, msg):
        """收到 /scan 消息时更新状态和时间"""
        self.scan_received = True
        self.last_scan_time = time()


    def mq2_callback(self, msg: Bool):
        """记录 mq2 传感器状态"""
        self.mq2_active = msg.data


    def timer_callback(self):
        """每 20ms 执行一次，更新灯光状态"""
        # 检查 /scan 是否超时
        if time() - self.last_scan_time > self.scan_timeout and self.scan_received:
            self.scan_received = False
            # print("change")

        # 逻辑判断
        if self.mq2_active:
            step = 40   # 快速呼吸
        elif not self.scan_received:
            step = 8    # 慢速呼吸
        else:
            step = 0    # 熄灭

        # 呼吸灯亮度变化
        if step > 0:
            self.pwm_value += self.direction * step
            if self.pwm_value >= 398:
                self.pwm_value = 398
                self.direction = -1
            elif self.pwm_value <= 1:
                self.pwm_value = 1
                self.direction = 1
        else:
            self.pwm_value = 1  # 熄灭

        # 发布 PWM 值
        msg = UInt16()
        msg.data = self.pwm_value
        self.pub_pwm.publish(msg)
        self.timer_check_callback()


def main(args=None):
    rclpy.init(args=args)
    node = BreathingLightNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.end()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
