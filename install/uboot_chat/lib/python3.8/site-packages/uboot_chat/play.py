import pygame
import sys
import argparse
import os

def play_audio(file_path):
    """
    使用 pygame 播放音频文件
    :param file_path: 音频文件路径
    """
    # 初始化 pygame 模块
    pygame.mixer.init()

    try:
        # 加载音频文件
        pygame.mixer.music.load(file_path)
        print(f"正在播放音频文件：{file_path}")

        # 播放音频
        pygame.mixer.music.play()

        # 等待音频播放完成
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        print("音频播放完成！")
    except pygame.error as e:
        print(f"播放音频时出错：{e}")
    finally:
        # 退出 pygame 模块
        pygame.mixer.quit()

if __name__ == "__main__":
    # 使用 argparse 解析命令行参数
    parser = argparse.ArgumentParser(description="使用 pygame 播放音频文件")
    parser.add_argument("file_path", type=str, help="音频文件路径")
    args = parser.parse_args()

    # 获取命令行参数中的音频文件路径
    file_path = args.file_path

    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"错误：文件 {file_path} 不存在！")
        sys.exit(1)

    # 播放音频
    play_audio(file_path)
