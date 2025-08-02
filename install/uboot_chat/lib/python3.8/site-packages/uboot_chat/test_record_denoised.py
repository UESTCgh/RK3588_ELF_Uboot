import sounddevice as sd
import numpy as np
import wave
from scipy.signal import butter, lfilter

# ======================
# 参数设置
# ======================
fs = 44100                  # 采样率（Hz）
duration = 5                # 录音时长（秒）
filename = "voice_stereo_filtered.wav"  # 输出文件名
channels = 2                # 双声道
dtype = 'int16'             # 采样格式

# ======================
# 带通滤波器设计（80~8000Hz）
# ======================
def bandpass_filter(data, lowcut=80, highcut=8000, fs=44100, order=6):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, data)

# ======================
# 开始录音
# ======================
print("开始录音…")
recording = sd.rec(
    int(duration * fs),
    samplerate=fs,
    channels=channels,
    dtype=dtype
)
sd.wait()
print("录音结束")

# ======================
# 标准化并滤波
# ======================
# int16 -> float32
audio = recording.astype(np.float32) / 32768

# 对每个声道独立滤波
filtered = np.zeros_like(audio)
for ch in range(channels):
    filtered[:, ch] = bandpass_filter(audio[:, ch], lowcut=80, highcut=8000, fs=fs)

# int16化并保存
filtered_int16 = np.clip(filtered * 32768, -32768, 32767).astype(np.int16)
with wave.open(filename, 'wb') as wf:
    wf.setnchannels(channels)
    wf.setsampwidth(2)
    wf.setframerate(fs)
    wf.writeframes(filtered_int16.tobytes())

print(f"已保存滤波后双声道人声音频：{filename}")
