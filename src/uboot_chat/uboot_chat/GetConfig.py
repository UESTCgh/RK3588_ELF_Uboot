from pydub import AudioSegment
import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="tkinter")

def get_audio_info(file_path):
    print(f"===== {file_path} =====")
    try:
        # 使用 pydub 加载音频文件
        audio = AudioSegment.from_file(file_path)
        
        # 获取音频的基本信息
        print("Using pydub:")
        print(f"  Format: {os.path.splitext(file_path)[1][1:]}")  # 文件扩展名作为格式
        print(f"  Channels: {audio.channels}")
        print(f"  Sample Rate: {audio.frame_rate} Hz")
        print(f"  Bit Depth: {audio.sample_width * 8} bits")
        print(f"  Duration: {audio.duration_seconds:.2f} seconds")
        print(f"  Max Volume: {audio.max_dBFS:.2f} dBFS")
        print(f"  RMS Volume: {audio.rms:.2f}")
        print(f"  Mean Volume: {audio.dBFS:.2f} dBFS")
        
        # 如果是双声道，分析左右声道的音量差异
        if audio.channels == 2:
            left_channel = audio.split_to_mono()[0]
            right_channel = audio.split_to_mono()[1]
            
            print("\nStereo Channel Analysis:")
            print(f"  Left Channel Max Volume: {left_channel.max_dBFS:.2f} dBFS")
            print(f"  Right Channel Max Volume: {right_channel.max_dBFS:.2f} dBFS")
            
            # 获取左右声道的时域信号
            left_samples = np.array(left_channel.get_array_of_samples())
            right_samples = np.array(right_channel.get_array_of_samples())
            
            # 绘制时域信号
            plt.figure(figsize=(12, 6))
            plt.plot(left_samples, label='Left Channel')
            plt.plot(right_samples, label='Right Channel')
            plt.title(f'{file_path} Waveform')
            plt.xlabel('Sample Index')
            plt.ylabel('Amplitude')
            plt.legend()
            plt.show()
        
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
    print("")

if __name__ == "__main__":
    # 使用 argparse 解析命令行参数
    parser = argparse.ArgumentParser(description="获取音频文件的详细信息")
    parser.add_argument("files", nargs="+", help="音频文件路径列表")
    args = parser.parse_args()

    # 遍历命令行输入的文件路径
    for file_path in args.files:
        if os.path.exists(file_path):
            get_audio_info(file_path)
        else:
            print(f"File {file_path} does not exist!\n")
