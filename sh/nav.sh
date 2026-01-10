#!/bin/bash

# 捕获 Ctrl+C（SIGINT）并终止所有子进程
trap 'echo "终止中..."; kill 0; exit' SIGINT

# 启动 SLAM
ros2 launch fishbot_navigation2 navigation2.launch.py

# 等待所有子进程退出
wait
