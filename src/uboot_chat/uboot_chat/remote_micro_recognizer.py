import queue
import sounddevice as sd
import re
import pkg_resources
from time import sleep
import numpy as np
from array import array
import socket
import os
import sys
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int16MultiArray, Bool


# 获取当前脚本的绝对路径
current_file_path = os.path.abspath(__file__)
# 获取当前脚本所在的目录
current_dir = os.path.dirname(current_file_path)
sys.path.append(current_dir)


from calibrate import CalibratorGPT

server_url = "passport.xfyun.cn"

def check_internet_connection(url=server_url, port=443):
    try:
        # 尝试连接到指定的网址和端口
        socket.create_connection((url, port), timeout=5)
        print(f"<-Mic Recognizer: 已连接到 {url}，已启用GPT修正语音识别结果->")
        return True
    except OSError:
        print(f"<-Mic Recognizer: 无法连接到 {url}，仅使用本地模型识别->")
        return False


class MicRecognizer(Node):
    def __init__(self, debug=False):
        super().__init__("MicRecognizer_server")
        self.device_info = sd.query_devices(None, 'input')
        # print(self.device_info)
        self._samplerate = int(self.device_info["default_samplerate"])
        print(f"sample rate: {self._samplerate}hz")
        self.rec_result = queue.Queue()
        self.work = True
        self.listen = True
        self.use_GPT = check_internet_connection()
        self.calibrator = CalibratorGPT()
        self.debug = debug

        self.publisher = self.create_publisher(Int16MultiArray, '/micro', 10)
        self.subscription_listen = self.create_subscription(Bool, '/chat_switch', self.chat_switch_callback, 10)
        self.subscription_listen = self.create_subscription(String, '/recognizer', self.recognizer_callback, 10)

    def _callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if self.listen:
            msg = Int16MultiArray()
            # print(np.frombuffer(indata, dtype=np.int16).tolist())
            msg.data = np.frombuffer(indata, dtype=np.int16).tolist() # 转成字节数组
            self.publisher.publish(msg)
    
    def chat_switch_callback(self, msg):
        if msg.data:
            self.open_ear()
        else:
            self.close_ear()

    def recognizer_callback(self, msg: String):
        text = msg.data
        if self.debug:
            print('1' + text)
        text = re.sub(r'\s+', '', text)
        if self.debug:
            print('2' + text)
        if len(text) > 1:
            if text[0] == "我":
                text = text[1:]
            if self.debug:
                print('vosk:' + text)
            if self.use_GPT:
                calibrated_text = self.calibrator.contact(text)
                if len(calibrated_text) < 1.5*len(text):
                    text = calibrated_text
            if self.debug:
                print('CalibratorGPT:' + text)
            self.rec_result.put(text)


    def start(self):
        self.open_ear()
        with sd.RawInputStream(samplerate=self._samplerate, dtype="int16", channels=1, blocksize=1024,
                               callback=self._callback, device=self.device_info['name']):
            print('<-Mic Recognizer Working...->')
            rclpy.spin(self)

    def close_ear(self):
        self.listen = False

    def open_ear(self):
        self.listen = True
        while not self.rec_result.empty():
            sleep(0.001)
            self.rec_result.get()

    def end(self):
        self.close_ear()
        self.calibrator.end()
        self.destroy_node()
        print('<-Mic Recognizer END->')


def main():
    rclpy.init()
    recognizer = MicRecognizer(True)
    try:
        recognizer.start()
    except KeyboardInterrupt:
        recognizer.end()
    finally:
        rclpy.shutdown() # 关闭ROS2
        
        
if __name__ == '__main__':
    main()


