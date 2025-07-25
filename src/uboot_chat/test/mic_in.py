import sounddevice as sd
import soundfile as sf
import numpy as np
import queue
import time

# 配置参数
device_index = 1
samplerate = 16000
channels = 2 #核心 取左侧
duration = 5
filename = "output.wav"

print(f"🎙️ 开始录音 {duration} 秒，并显示实时音量...")

# 初始化录音缓冲队列
q = queue.Queue()
recorded_frames = []

def callback(indata, frames, time_info, status):
    if status:
        print("⚠️ 状态:", status)
    q.put(indata.copy())  # 保存数据
    # 计算音量强度
    volume = np.linalg.norm(indata) * 10
    print("🎧 音量强度: {:>6.2f}".format(volume))

try:
    with sd.InputStream(device=device_index,
                        samplerate=samplerate,
                        channels=channels,
                        dtype='int16',
                        blocksize=1024,
                        callback=callback):
        start_time = time.time()
        while time.time() - start_time < duration:
            frame = q.get()
            recorded_frames.append(frame)

    # 合并所有帧，保存为 wav 文件
    recording = np.concatenate(recorded_frames, axis=0)
    sf.write(filename, recording, samplerate)
    print(f" 录音完成，已保存为: {filename}")

except Exception as e:
    print(" 错误:", str(e))
