from aip import AipSpeech
from pygame import mixer, time
import os
from requests.exceptions import ConnectionError
import os
import sys

# 获取当前脚本的绝对路径
current_file_path = os.path.abspath(__file__)
# 获取当前脚本所在的目录
current_dir = os.path.dirname(current_file_path)
sys.path.append(current_dir)

from OneToTwo import convert_mono_to_stereo as convert

# 百度AI平台注册后获得的APP_ID, API_KEY, SECRET_KEY
APP_ID = '118420416'
API_KEY = 'ii05YqEXyfODmqht6bzBx8es'
SECRET_KEY = 'A6OywRPNzIeHi7LIORg8j1ByDsxfG990'



class Speech:
    def __init__(self):
        self._client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        self.vol = 10  # 音量
        self.speed = 6  # 语速
        self.pit = 5  # 语调
        self.per = 5003  # 发音人类型
        self.output_name = "output.mp3"
        self.work = True

        mixer.init()
        self.talk('UBOOT初始化完成')
        print('<-Speech working...->')

    def talk(self, sentence):
        try:
            result = self._client.synthesis(
                sentence,
                'zh',  # 语言
                1,     # 发音人选择，0为默认
                {
                    'vol': self.vol,  # 音量
                    'spd': self.speed,  # 语速
                    'pit': self.pit,  # 音调
                    'per': self.per,   # 发音人类型
                }
            )
        except ConnectionError:
            print("<-Speech: 网络连接错误，请重试->")
            return

        if not isinstance(result, dict):
            with open(current_dir+'/'+self.output_name, "wb") as f:
                f.write(result)
            convert(current_dir+'/'+self.output_name, current_dir+'/'+'C2M'+self.output_name, False)
            try:
                # 加载音频文件、播放音频
                sound = mixer.Sound(current_dir+'/'+'C2M'+self.output_name)
                sound.play()

                # 等待音频播放完毕
                while mixer.get_busy() and self.work:
                    time.delay(100)
            except Exception as e:
                print(f"播放音频时出错: {e}")

        else:
            print("语音合成失败:", result)

    def end(self):
        mixer.quit()
        # 删除临时文件
        self.work = False
        try:
            os.remove(self.output_name)
            pass
        except FileNotFoundError:
            pass
        print('<-Speech END->')


def main():
    speech = Speech()
    try:
        speech.talk('hello, 语音合成')
    except KeyboardInterrupt:
        speech.end()
    finally:
        pass
    
    
    
if __name__ == '__main__':
    main()
