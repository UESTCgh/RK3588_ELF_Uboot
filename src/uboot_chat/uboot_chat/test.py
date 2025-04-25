import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

# 录音参数
duration = 5  # 录音时长（秒）
sample_rate = 44100  # 采样率
channels = 2  # 声道数（单声道为1，立体声为2）
dtype = 'int16'  # 数据类型

print("开始录音...")

# 开始录音
recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, dtype=dtype)
sd.wait()  # 等待录音完成

print("录音完成。")

# 获取录音数据并归一化（因为 int16 的范围是 -32768 到 32767）
recording_normalized = recording / np.iinfo(dtype).max

# 保存为 WAV 文件
filename = "recording.wav"
write(filename, sample_rate, (recording_normalized * 32767).astype(dtype))

print(f"录音已保存为 {filename}")