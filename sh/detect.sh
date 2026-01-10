#!/bin/bash

# 捕获 Ctrl+C（SIGINT）并终止所有子进程
trap 'echo "终止中..."; kill 0; exit' SIGINT

ros2 run yolo_v5 start
# 等待所有子进程退出
wait
