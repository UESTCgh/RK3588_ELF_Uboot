#!/bin/bash

# 捕获 Ctrl+C（SIGINT）并终止所有子进程
trap 'echo "终止中..."; kill 0; exit' SIGINT

echo "语音模块初始化中...."
ros2 run uboot_chat chat & sleep 20
echo "任务调度...."
ros2 run task_scheduler start 

# 等待所有子进程退出
wait
