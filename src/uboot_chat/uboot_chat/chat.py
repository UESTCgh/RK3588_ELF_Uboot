import os.path
import sys

# 获取当前脚本的绝对路径
current_file_path = os.path.abspath(__file__)
# 获取当前脚本所在的目录
current_dir = os.path.dirname(current_file_path)
sys.path.append(current_dir)


from sparkModel import SparkGPT
from micro_recognizer import MicRecognizer
from speechGC import Speech
import threading
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from time import sleep


class Chat:
    def __init__(self):
        self.recognizer = MicRecognizer()
        self.recognizer_thread = threading.Thread(target=self.recognizer.start)
        self.chat_core = SparkGPT()
        self.speech = Speech()
        self.work = True

    def start(self):
        self.work = True
        self.recognizer_thread.start()
        while self.work:
            question = self.recognizer.rec_result.get()
            print('顾客：' + question)
            answer = self.chat_core.contact(question)
            self.speech.talk(answer)
            print('征服者机器人：'+answer)
            self.recognizer.rec_result.task_done()
            

    def end(self):
        self.work = False
        self.recognizer.end()
        self.chat_core.end()
        self.speech.end()


class ChatPublisher(Node):
    def __init__(self):
        super().__init__('chat_server')
        self.chat = Chat()
        self.chat_thread = threading.Thread(target=self.chat.start)
        self.publisher_ = self.create_publisher(String, '/chat', 10)
        self.subscription = self.create_subscription(String, '/uboot', self.listener_callback, 10)
        self.timer_ = self.create_timer(1.0, self.timer_callback)
        self.chat_thread.start()

    def listener_callback(self, msg):
        print(msg.data)

    def timer_callback(self):
        msg = String()
        msg.data = "0"
        self.publisher_.publish(msg)

    def msg_to_uboot(self, value:str):
        msg = String()
        msg.data = value
        self.publisher_.publish(msg)
    
    def end(self):
        self.chat.end()


def main(args=None):
    rclpy.init(args=args)
    chat_node = ChatPublisher()
    try:
        rclpy.spin(chat_node) # 启动节点的事件循环
    except KeyboardInterrupt:
        chat_node.end()
        chat_node.destroy_node() # 清理并关闭节点
    finally:
        rclpy.shutdown() # 关闭ROS2


if __name__ == '__main__':
    main()