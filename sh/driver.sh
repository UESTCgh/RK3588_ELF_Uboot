#!/bin/bash

# 捕获 Ctrl+C（SIGINT）并终止所有子进程
trap 'echo "终止中..."; kill 0; exit' SIGINT

# 启动 rplidar_ros
ros2 launch rplidar_ros rplidar_a1_launch.py &
sleep 2

# 启动 fishbot_bringup
ros2 launch fishbot_bringup fishbot_bringup.launch.py &
sleep 2

# 启动 micro_ros_agent
ros2 run micro_ros_agent micro_ros_agent serial -b 921600 --dev /dev/robot -v6 &
sleep 2

# 等待所有子进程退出
wait
