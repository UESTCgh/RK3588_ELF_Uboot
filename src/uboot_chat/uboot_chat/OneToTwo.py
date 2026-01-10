from pydub import AudioSegment
import argparse
import os

def normalize_audio(audio, target_dBFS, showPrint=True):
    """
    将音频的最大音量调整到指定的 dBFS 值
    :param audio: pydub AudioSegment 对象
    :param target_dBFS: 目标最大音量（单位：dBFS）
    :return: 调整后的音频
    """
    if showPrint:
        print(f"  Current Max Volume: {audio.max_dBFS:.2f} dBFS")
    change_in_dBFS = target_dBFS - audio.max_dBFS
    normalized_audio = audio.apply_gain(change_in_dBFS)
    if showPrint:
        print(f"  New Max Volume: {normalized_audio.max_dBFS:.2f} dBFS")
    return normalized_audio

def convert_mono_to_stereo(input_file, output_file, showPrint=True, sample_rate=44100, bit_depth=16):
    """
    将单声道音频转换为双声道，并调整左右声道的最大音量
    :param input_file: 输入音频文件路径
    :param output_file: 输出 WAV 文件路径
    :param sample_rate: 采样率（Hz）
    :param bit_depth: 位深（16 表示 int16 格式）
    """
    try:
        # 加载单声道音频
        mono_audio = AudioSegment.from_file(input_file)
        
        # 确保输入是单声道
        if mono_audio.channels != 1:
            print("输入音频不是单声道。")
            return
        
        # 调整单声道音频的最大音量到 -18 dBFS
        left_channel = normalize_audio(mono_audio, -30.0, showPrint)
        
        # 复制左声道到右声道
        right_channel = left_channel
        
        # 调整右声道的最大音量到 0 dBFS
        right_channel = normalize_audio(right_channel, 0.0, showPrint)
        
        # 合并左右声道为双声道
        stereo_audio = AudioSegment.from_mono_audiosegments(left_channel, right_channel)
        
        # 转换为指定的采样率和位深
        stereo_audio = stereo_audio.set_frame_rate(sample_rate)
        stereo_audio = stereo_audio.set_sample_width(bit_depth // 8)
        
        # 保存为 WAV 文件
        stereo_audio.export(output_file, format="wav")
        if showPrint:
            print(f"音频文件已成功转换为双声道 WAV 格式，保存到 {output_file}")
    
    except Exception as e:
        print(f"转换音频时出错：{e}")

if __name__ == "__main__":
    # 使用 argparse 解析命令行参数
    parser = argparse.ArgumentParser(description="将单声道音频转换为双声道，并调整左右声道的最大音量")
    parser.add_argument("input_file", type=str, help="输入音频文件路径")
    parser.add_argument("output_file", type=str, help="输出 WAV 文件路径")
    parser.add_argument("--sample_rate", type=int, default=44100, help="采样率（Hz，默认为 44100）")
    parser.add_argument("--bit_depth", type=int, default=16, help="位深（单位：bits，默认为 16）")
    args = parser.parse_args()

    # 获取命令行参数中的输入和输出文件路径
    input_file = args.input_file
    output_file = args.output_file
    sample_rate = args.sample_rate
    bit_depth = args.bit_depth

    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"错误：文件 {input_file} 不存在！")
        exit(1)

    # 转换音频
    convert_mono_to_stereo(input_file, output_file, sample_rate, bit_depth)
