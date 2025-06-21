import rclpy
from rclpy.node import Node
from sensor.msg import DeviceStatus
from random import gauss, choice

class StatusPub(Node):
    def __init__(self):
        super().__init__('test_statusPub_server')
        self.msg = DeviceStatus()
        self.msg.temperature = 24.0
        self.msg.humidity = 60.0
        self.msg.presence = 1
        self.msg.mq2 = 1
        self.msg.val = 0
        self.pub = self.create_publisher(DeviceStatus, '/from_core', 10)
        self.timer_ = self.create_timer(1, self.time_callback)
        print('<-Status publisher: working...->')
    
    def time_callback(self):
        self.msg.humidity += gauss(0, 1)
        self.msg.temperature += gauss(0, 0.5)
        self.msg.presence = choice([0,1])
        self.msg.mq2 = choice([0,1])
        self.pub.publish(self.msg)

def main():
    rclpy.init()
    test_node = StatusPub()
    try:
        rclpy.spin(test_node)
    except KeyboardInterrupt:
        test_node.destroy_node() # 清理并关闭节点
    finally:
        rclpy.shutdown() # 关闭ROS2


if __name__ == '__main__':
    main()