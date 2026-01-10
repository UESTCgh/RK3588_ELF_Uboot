import sounddevice as sd
import numpy as np
import wave

# 设置录音参数
fs = 44100          # 采样率（Hz）
duration = 3        # 录制时长（秒）
filename = "record.wav"  # 输出文件名
channels = 2        # 声道数（1=单声道，2=立体声）
dtype = 'int16'     # 音频数据格式（WAV 文件常用格式）

print("开始录音...")
# 录制音频
recording = sd.rec(
    int(duration * fs),  # 采样点数 = 时长 × 采样率
    samplerate=fs,
    channels=channels,
    dtype=dtype
)
sd.wait()  # 等待录制完成
print("录音结束")

# 使用 wave 保存为 WAV 文件
with wave.open(filename, 'wb') as wav_file:
    wav_file.setnchannels(channels)      # 设置声道数
    wav_file.setsampwidth(2)             # 采样宽度（字节），int16=2字节
    wav_file.setframerate(fs)            # 采样率
    wav_file.writeframes(recording.tobytes())  # 写入音频数据

print(f"音频已保存为 {filename}")
