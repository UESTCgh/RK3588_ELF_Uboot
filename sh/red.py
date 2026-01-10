#!/usr/bin/env python3
import rclpy
import time
from rclpy.node import Node
from std_msgs.msg import UInt16, Bool
from sensor_msgs.msg import LaserScan


class BreathingLightNode(Node):
    def __init__(self):
        super().__init__('breathing_light_controller')
        
        # 订阅两个话题
        self.sub_scan = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.sub_mq2 = self.create_subscription(Bool, '/mq2', self.mq2_callback, 10)
        
        # 发布 PWM
        self.pub_pwm = self.create_publisher(UInt16, '/pwm', 10)

        # 状态
        self.scan_received = False  
        self.last_scan_time = 0.0   # 最近一次收到 /scan 消息的时间
        self.scan_timeout = 0.1     # 100ms 超时
        self.mq2_active = False     
        
        # 呼吸灯参数
        self.pwm_value = 1
        self.direction = 1  # 1: 增亮, -1: 变暗

        # 定时器（循环控制呼吸灯）
        self.timer = self.create_timer(0.02, self.timer_callback)


    def scan_callback(self, msg):
        """收到 /scan 消息时更新状态和时间"""
        self.scan_received = True
        self.last_scan_time = time.time()


    def mq2_callback(self, msg: Bool):
        """记录 mq2 传感器状态"""
        self.mq2_active = msg.data


    def timer_callback(self):
        """每 20ms 执行一次，更新灯光状态"""
        # 检查 /scan 是否超时
        if time.time() - self.last_scan_time > self.scan_timeout and self.scan_received:
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


def main(args=None):
    rclpy.init(args=args)
    node = BreathingLightNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
