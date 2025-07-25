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
        print(f"<-Mic Recognizer: 已启用GPT修正语音识别结果->")
        return True
    except OSError:
        print(f"<-Mic Recognizer: 无法连接到 GPT，仅使用本地模型识别->")
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
        self.debug = debug
        self.channel = -1  # 主通道（立体声时使用）
        
        # 采集噪声样本（自动匹配正式录音的声道处理）
        print("【正在采集噪声样本，请保持安静...】")
        noise_recording = sd.rec(
            int(1 * self._samplerate),
            samplerate=self._samplerate,
            channels=self.device_info['max_input_channels'],  # 和正式录音一致
            dtype='int16'
        )
        sd.wait()
        
        # 统一转单声道（逻辑和 _callback 一致）
        if self.device_info['max_input_channels'] > 1:
            noise_recording = noise_recording.reshape(-1, 2)
            self.channel = np.argmax([np.sum(noise_recording[:, i]**2) for i in range(2)])
            noise_recording = noise_recording[:, self.channel]
        
        # 保存噪声样本（归一化）
        self.noise_sample = noise_recording.flatten().astype(np.float32) / 32768.0

    def _callback(self, indata, frames, time, status):
        audio_data = np.frombuffer(indata, dtype=np.int16)
        
        # 立体声转单声道（和噪声样本逻辑一致）
        if self.device_info['max_input_channels'] > 1:
            audio_data = audio_data.reshape(-1, 2)
            if self.channel < 0:  # 如果未初始化，选择能量更高的通道
                self.channel = np.argmax([np.sum(audio_data[:, i]**2) for i in range(2)])
            audio_data = audio_data[:, self.channel]
        
        # 降噪处理
        audio_float = audio_data.astype(np.float32) / 32768.0
        reduced_noise = nr.reduce_noise(
            y=audio_float,
            y_noise=self.noise_sample,
            sr=self._samplerate,
            stationary=True,
            prop_decrease=0.7
        )
        processed_data = (reduced_noise * 32767).astype(np.int16).tobytes()
        self._q.put(processed_data)
        
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


