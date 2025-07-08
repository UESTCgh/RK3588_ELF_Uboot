from pydub import AudioSegment

def get_audio_info(file_path):
    print(f"===== {file_path} =====")
    # 使用 pydub 获取音频信息
    audio = AudioSegment.from_file(file_path)
    print("Using pydub:")
    #print(f"  Format: {audio.format}")
    print(f"  Channels: {audio.channels}")
    print(f"  Sample Rate: {audio.frame_rate} Hz")
    print(f"  Bit Depth: {audio.sample_width * 8} bits")
    print(f"  Duration: {audio.duration_seconds:.2f} seconds")
    print(f"  Max Volume: {audio.max_dBFS:.2f} dBFS")

    print("")

# 示例用法
file_path = ["output.mp3", 'test.wav', "ouput.wav", "output_vol.wav", "output_vol.mp3", "output_vol_2.wav"]  # 替换为你的音频文件路径
for i in file_path:
    try:
        get_audio_info(i)
    except FileNotFoundError:
        print("File don't exist!\n")
