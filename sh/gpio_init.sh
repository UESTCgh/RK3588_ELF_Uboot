#!/bin/bash

GPIO=109
GPIO_PATH="/sys/class/gpio/gpio$GPIO"

# 只导出一次
if [ ! -d "$GPIO_PATH" ]; then
    echo $GPIO | sudo tee /sys/class/gpio/export > /dev/null
    sleep 0.2
fi

# 设置方向
echo in | sudo tee "$GPIO_PATH/direction" > /dev/null &

# 设置权限
sudo chown root:gpio "$GPIO_PATH"/
sudo chmod 777 "$GPIO_PATH"/
