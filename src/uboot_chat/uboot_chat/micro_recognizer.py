import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import re
import pkg_resources
from time import sleep
import numpy as np
import socket
import os
import sys

# 获取当前脚本的绝对路径
current_file_path = os.path.abspath(__file__)
# 获取当前脚本所在的目录
current_dir = os.path.dirname(current_file_path)
sys.path.append(current_dir)


from calibrate import CalibratorGPT


# resource_path = pkg_resources.resource_filename(__name__, '/vosk-model-small-cn-0.22')
resource_path = current_dir + '/vosk-model-small-cn-0.22'
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


class MicRecognizer:
    def __init__(self, debug=False):
        self._q = queue.Queue()
        self.device_info = sd.query_devices(1, 'input')
        self._samplerate = int(self.device_info["default_samplerate"])
        self._rec = KaldiRecognizer(Model(resource_path), self._samplerate)
        self.rec_result = queue.Queue()
        self.work = True
        self.listen = True
        self.use_GPT = check_internet_connection()
        self.calibrator = CalibratorGPT()
        self.channel = -1
        self.debug = debug

    def _callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if self.device_info['max_input_channels'] == 1:
            self._q.put(bytes(indata))
        else:
            # 将立体声(双通道)转换为单声道
            # 先将缓冲区转换为numpy数组
            audio_data = np.frombuffer(indata, dtype=np.int16)
            # 重塑为双通道数组
            audio_data = audio_data.reshape(-1, 2)
            # 得到单声道
            if self.channel < 0:
                MSE = [np.sum(audio_data[:, i] ** 2) for i in range(audio_data.shape[1])]
                self.channel = MSE.index(max(MSE))
            mono_data = audio_data[:, self.channel]
            self._q.put(mono_data.tobytes())

    def start(self):
        debug = self.debug
        self.work = True
        self.open_ear()
        with sd.RawInputStream(samplerate=self._samplerate, dtype="int16", channels=self.device_info['max_input_channels'],
                               callback=self._callback, device=self.device_info['name']):
            print('<-Mic Recognizer Working...->')

            try:
                while self.work:
                    data = self._q.get()
                    if debug:
                        # volume = np.linalg.norm(np.frombuffer(data, dtype='int16')) / 1000
                        # print("音量:", volume)
                        pass
                    if not self.listen:
                        sleep(0.001)
                        continue
                    if self._rec.AcceptWaveform(data):
                        text = eval(self._rec.Result())["text"]
                        if debug:
                            print('1' + text)
                        text = re.sub(r'\s+', '', text)
                        if debug:
                            print('2' + text)
                        if len(text) > 1:
                            if debug:
                                print('vosk:' + text)
                            if self.use_GPT:
                                calibrated_text = self.calibrator.contact(text)
                                if len(calibrated_text) < 1.5*len(text):
                                    text = calibrated_text
                            if debug:
                                print('CalibratorGPT:' + text)
                            self.rec_result.put(text)
            except KeyboardInterrupt:
                self.end()

    def close_ear(self):
        self.listen = False

    def open_ear(self):
        self.listen = True
        while not self.rec_result.empty():
            sleep(0.001)
            self.rec_result.get()

    def end(self):
        self.work = False
        self.calibrator.end()
        print('<-Mic Recognizer END->')


def main():
    recognizer = MicRecognizer(True)
    try:
        recognizer.start()
    except KeyboardInterrupt:
        recognizer.end()
    finally:
        pass
        
        
if __name__ == '__main__':
    main()


