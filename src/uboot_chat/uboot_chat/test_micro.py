import os
import wave
import json
from vosk import Model, KaldiRecognizer
import pkg_resources


resource_path = pkg_resources.resource_filename(__name__, '/vosk-model-small-cn-0.22')

class VoskSpeechRecognizer:
    def __init__(self, model_path):
        """
        初始化语音识别器
        :param model_path: Vosk模型路径
        """
        if not os.path.exists(model_path):
            print(f"模型路径不存在: {model_path}")
            raise FileNotFoundError(f"Vosk模型目录不存在: {model_path}")

        self.model = Model(model_path)
        self.sample_rate = None
        self.recognizer = None

    def recognize_wav_file(self, wav_path):
        """
        识别WAV格式的录音文件
        :param wav_path: WAV文件路径
        :return: 识别结果文本
        """
        if not os.path.exists(wav_path):
            raise FileNotFoundError(f"音频文件不存在: {wav_path}")

        # 打开WAV文件
        with wave.open(wav_path, "rb") as wf:
            # 检查音频格式
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2:
                raise ValueError("音频文件必须是单声道WAV格式(PCM 16位)")

            self.sample_rate = wf.getframerate()
            self.recognizer = KaldiRecognizer(self.model, self.sample_rate)

            # 读取音频数据并进行识别
            results = []
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    results.append(result.get("text", ""))

            # 获取最终结果
            final_result = json.loads(self.recognizer.FinalResult())
            results.append(final_result.get("text", ""))

            return " ".join(filter(None, results))


if __name__ == "__main__":
    # 使用示例
    try:
        # 替换为你的Vosk模型路径
        MODEL_PATH = resource_path  # 中文小模型示例
        # 替换为你要识别的WAV文件路径
        AUDIO_FILE = "test_local.wav"

        recognizer = VoskSpeechRecognizer(MODEL_PATH)
        text = recognizer.recognize_wav_file(AUDIO_FILE)

        print("识别结果:")
        print(text)

    except Exception as e:
        print(f"发生错误: {str(e)}")