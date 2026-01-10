#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt16

class PwmPublisher(Node):
    def __init__(self):
        super().__init__('pwm_publisher')
        self.publisher_ = self.create_publisher(UInt16, '/pwm', 10)
        self.timer = self.create_timer(0.001, self.timer_callback)  # 1ms周期
        self.value = 0
        self.max_value = 399
        self.direction = 1  # 1 表示递增，-1 表示递减

    def timer_callback(self):
        msg = UInt16()
        msg.data = self.value
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {msg.data}')
        
        # 按方向变化
        self.value += self.direction

        # 到达边界就反转方向
        if self.value >= self.max_value:
            self.value = self.max_value
            self.direction = -1
        elif self.value <= 0:
            self.value = 0
            self.direction = 1

def main(args=None):
    rclpy.init(args=args)
    node = PwmPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
