import os.path
import sys

# 获取当前脚本的绝对路径
current_file_path = os.path.abspath(__file__)
# 获取当前脚本所在的目录
current_dir = os.path.dirname(current_file_path)
sys.path.append(current_dir)

from sparkModel import SparkGPT
from localModel import LocalGPT
from micro_recognizer import MicRecognizer
from speechGC import Speech
import threading
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool, Float32
from time import sleep


class Chat:
    def __init__(self,subtitle_publisher, mode=1):
        """
        mode=1 使用本地GPT模型
        mode=0 使用讯飞spark4.0 Ultra模型
        """
        self.subtitle_pub = subtitle_publisher
        self.recognizer = MicRecognizer()
        self.recognizer_thread = threading.Thread(target=self.recognizer.start)
        if mode:
            self.chat_core = LocalGPT()
        else:
            self.chat_core = SparkGPT()
        self.speech = Speech()
        self.work = True

    def start(self):
        self.work = True
        self.recognizer_thread.start()
        while self.work:
            # question = input('顾客：' )
            if self.recognizer.rec_result.empty():
                sleep(0.1)
                continue
            question = self.recognizer.rec_result.get()
            print('顾客：' + question)
            answer = self.chat_core.contact(question)
            if answer:
                self.talk(answer)
            self.recognizer.rec_result.task_done()
            
    def talk(self, msg):
        subtitle_msg = String()
        subtitle_msg.data = msg
        self.subtitle_pub.publish(subtitle_msg)
        print('[字幕] 已发布：', msg)

        self.recognizer.close_ear()
        self.speech.talk(msg)
        self.recognizer.open_ear()
        print('UBOOT机器人：'+msg)

    def end(self):
        self.work = False
        self.recognizer.end()
        self.chat_core.end()
        self.speech.end()
        self.recognizer_thread.join()


class ChatPublisher(Node):
    def __init__(self, mode=1):
        """
        mode=1 使用本地GPT模型
        mode=0 使用讯飞spark4.0 Ultra模型
        """
        super().__init__('chat_server')
        self.subtitle_pub = self.create_publisher(String, '/subtitle', 10)  # 创建字幕发布器
        self.chat = Chat(self.subtitle_pub, mode) 
        self.chat_thread = threading.Thread(target=self.chat.start)
        self.publisher_ = self.create_publisher(String, '/chat', 10)
        self.subscription = self.create_subscription(String, '/uboot', self.listener_callback, 10)
        self.subscription_status_mq2 = self.create_subscription(Bool, '/mq2', self.mq2_status_callback, 10)
        self.subscription_status_temp = self.create_subscription(Float32, '/temp', self.temp_status_callback, 10)
        self.subscription_status_hum = self.create_subscription(Float32, '/hum', self.hum_status_callback, 10)
        self.T = 24  # 温度
        self.H = 68  # 湿度
        self.talk = False  # 说话标志位
        self.timer_ = self.create_timer(0.5, self.timer_callback)
        self.chat_thread.start()

    def listener_callback(self, msg):
        if str(msg.data) == 'back':
            self.chat.talk('尊敬的客人，我们已到达目标房间，本机将开始返回服务点')

    def mq2_status_callback(self, msg:Bool):
        if msg.data == True and self.talk==False:
            self.talk = True
            self.chat.talk('警告！有毒，快跑！')
            self.talk = False
       
        print(msg.data)
    
    def temp_status_callback(self, msg:Float32):
        self.T = msg.data
        print(self.T)
        
    def hum_status_callback(self, msg:Float32):
        self.H = msg.data
        print(self.H)

    def timer_callback(self):
        msg = String()
        if self.chat.chat_core.user_requirements.empty():
            msg.data = "0"
        else:
            requirement = str(self.chat.chat_core.user_requirements.get())
            if requirement.isdigit():
                msg.data = requirement
            else:
                msg.data = "0"
                self.talk_status(requirement)
            self.chat.chat_core.user_requirements.task_done()
        self.publisher_.publish(msg)

    def talk_status(self, status):
        if status == '温度':
            self.chat.talk(f'现在的环境温度为{self.T:.1f}度')
        else:
            self.chat.talk(f'现在的环境湿度为百分之{self.H:.1f}')

    def msg_to_uboot(self, value:str):
        msg = String()
        msg.data = value
        self.publisher_.publish(msg)
    
    def end(self):
        self.chat.end()
        self.chat_thread.join()

def main(args=None):
    rclpy.init(args=args)
    if len(sys.argv)>1:
        mode = sys.argv[1]
        if not mode.isdigit():
            print("[ERROR] python3 chat.py [mode=1]; mode=1, use ip: use local GPT; mode=0: use spark4.0 Ultra.")
            return
        chat_node = ChatPublisher(int(mode))
    else:
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
