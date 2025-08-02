#!/bin/bash

# 需要root权限

# 捕获 Ctrl+C（SIGINT）并终止所有子进程
trap 'echo "终止中..."; kill 0; exit' SIGINT

# 启动
echo start > /sys/class/remoteproc/remoteproc0/state &
sleep 1

# 启动 
echo rpmsg_chrdev > /sys/bus/rpmsg/devices/virtio0.rpmsg-openamp-demo-channel.-1.0/driver_override &
sleep 1

modprobe rpmsg_char

sudo chmod 666 /dev/rpmsg_ctrl0
sudo chmod 666 /dev/rpmsg0

# ros2 run sensor sensor_node 
ros2 run sensor openamp_core1

# 等待所有子进程退出
wait
