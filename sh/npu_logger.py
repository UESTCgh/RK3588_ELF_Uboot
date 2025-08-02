#!/usr/bin/env python3
import os
import time
from datetime import datetime
import stat

# 配置路径
NPU_LOAD_PATH = "/sys/kernel/debug/rknpu/load"
NPU_FREQ_PATH = "/sys/class/devfreq/fdab0000.npu/cur_freq"
OUTPUT_PATH = "/home/uboot/data/npu_status.txt"
INTERVAL = 0.5  # 秒数间隔

def read_file(path):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except Exception as e:
        return f"[ERROR reading {path}]: {e}"

def write_output(content):
    try:
        with open(OUTPUT_PATH, "w") as f:
            f.write(content)
        os.chmod(OUTPUT_PATH, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)  # 644
    except Exception as e:
        print(f"[ERROR writing to {OUTPUT_PATH}]: {e}")

def main():
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        load_info = read_file(NPU_LOAD_PATH)
        freq_info = read_file(NPU_FREQ_PATH)

        output = f"==== {timestamp} ====\n"
        output += f"{load_info}\n\n{freq_info}\n"
        write_output(output)

        time.sleep(INTERVAL)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("必须以 root 权限运行此脚本。")
        exit(1)
    main()
