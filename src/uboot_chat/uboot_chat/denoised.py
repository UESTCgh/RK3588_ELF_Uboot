import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.fft import fft, fftfreq

# 音频参数
device_info = sd.query_devices(1, 'input')
CHUNK = 1024  # 每次处理的样本数
CHANNELS = 2  # 双声道
RATE = int(device_info["default_samplerate"])  # 采样率
DTYPE = 'int16'  # 采样格式

# 创建图形和子图
plt.rcParams['toolbar'] = 'None'  # 隐藏工具栏
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# 初始化波形图
x = np.arange(0, CHUNK)
line_left, = ax1.plot(x, np.zeros(CHUNK), 'b', label='Left channels')
line_right, = ax1.plot(x, np.zeros(CHUNK), 'r', label='Right channels')
ax1.set_title('{} wave'.format(device_info['name']))
ax1.set_xlim(0, CHUNK)
ax1.set_ylim(-3276.8, 3276.8)  # 16位有符号整型范围
ax1.legend(loc='upper right')

# 初始化频谱图
n = CHUNK
freqs = fftfreq(n, 1/RATE)[:n//2]
line_fft_left, = ax2.semilogy(freqs, np.ones(n//2), 'b', label='Left channels')
line_fft_right, = ax2.semilogy(freqs, np.ones(n//2), 'r', label='Right channels')
ax2.set_title('freq')
ax2.set_xlim(20, RATE/2)  # 20Hz到Nyquist频率
ax2.set_ylim(1, 10**7)
ax2.legend(loc='upper right')

# 调整子图间距
plt.tight_layout()

# 创建音频流回调函数
def audio_callback(indata, frames, time, status):
    global audio_data
    audio_data = indata.copy()

# 初始化全局变量存储音频数据
audio_data = np.zeros((CHUNK, CHANNELS), dtype=DTYPE)

# 创建音频流
stream = sd.InputStream(
    samplerate=RATE,
    blocksize=CHUNK,
    channels=CHANNELS,
    dtype=DTYPE,
    callback=audio_callback,
    device=device_info['name']
)

def update(frame):
    # 分离左右声道
    left_channel = audio_data[:, 0]
    right_channel = audio_data[:, 1]
    
    # 更新波形图
    line_left.set_ydata(left_channel)
    line_right.set_ydata(right_channel)
    
    # 计算FFT并更新频谱图
    fft_left = np.abs(fft(left_channel))[:n//2]
    fft_right = np.abs(fft(right_channel))[:n//2]
    line_fft_left.set_ydata(fft_left)
    line_fft_right.set_ydata(fft_right)
    
    return line_left, line_right, line_fft_left, line_fft_right

# 启动音频流
stream.start()

# 创建动画
ani = FuncAnimation(fig, update, blit=True, interval=20)

plt.show()

# 清理
stream.stop()
stream.close()
