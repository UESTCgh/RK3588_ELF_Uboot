#!/bin/bash

# 启动所有任务并放入后台，禁用所有输出
#运控节点
echo "启动micro_ros_agent..."
ros2 run micro_ros_agent micro_ros_agent serial -b 921600 --dev /dev/ttyUSB1 -v6 > /dev/null 2>&1 &

#雷达节点
echo "启动RPLidar..."
ros2 launch rplidar_ros rplidar_a1_launch.py > /dev/null 2>&1 &

#fishbotTF节点
echo "启动fishbot_bringup..."
ros2 launch fishbot_bringup fishbot_bringup.launch.py > /dev/null 2>&1 &

# #建图节点
# echo "启动cartographer..."
# ros2 launch fishbot_cartographer cartographer.launch.py > /dev/null 2>&1 &

#控制节点
echo "启动键盘控制..."
ros2 run teleop_twist_keyboard teleop_twist_keyboard > /dev/null 2>&1 &

echo "所有任务已在后台启动"
