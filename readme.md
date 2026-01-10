# 关于Uboot代码仓库的说明
## 1.说明

### 1.1 分支说明

**gh/longhua_com** 分支为RK3588的代码分支

gh/pi_dev 为飞腾派的代码分支

**fishbot/ rplidar_ros/** 这两个部分需要根据不同的板子进行适配

### 1.2 目录说明

src/下面为各种ros功能包，实现导航建图，显示，驱动，任务调度等功能；

sh/为快速启动的代码；

其余为ROS2编译的产物。

## 2.快速启动

```
大模型
GPTserver qwen3_b
chat
yolo_npu
task

驱动
sensor
driver

UI
触摸屏
ui
电脑端
U 
I

无人车移动相关
slam
nav （分布式跑）
ros2 run teleop_twist_keyboard teleop_twist_keyboard

# 小车上跑
ros2 run micro_ros_agent micro_ros_agent serial -b 921600 --dev /dev/robot -v6

ros2 launch rplidar_ros rplidar_a1_launch.py

ros2 launch fishbot_bringup fishbot_bringup.launch.py

ros2 run usb_cam usb_cam_node_exe
 
ros2 run sensor sensor_node 
# 远程跑
ros2 run teleop_twist_keyboard teleop_twist_keyboard

ros2 launch fishbot_cartographer cartographer.launch.py
ros2 launch fishbot_navigation2 navigation2.launch.py

source install/setup.bash

# 保存地图
ros2 run nav2_map_server map_saver_cli --help
rqt_image_view
sudo chmod 777 /dev/i2c-2
ros2 run sensor sensor_node
```

### 3. 资料

UI代码仓库：https://github.com/UESTCgh/Ros_Qt5_Gui_App_uboot

小核代码仓库：https://github.com/uestc-uboot/Slave

网盘资料：

https://pan.baidu.com/s/18HntfsVP4sZnxScufqwzVQ 提取码: 65j6 

https://pan.baidu.com/s/1UL5CjBWfIaJbVWB8cuRv3Q 提取码: 28vs 
