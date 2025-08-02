sudo chmod 777 /dev/i2c-4
sudo python3 /home/uboot/data/ros2_uboot/sh/npu_logger.py&
# bash /home/uboot/data/ros2_uboot/sh/gpio_init.sh&
cd /home/uboot/data/ros2_uboot/build/sensor
# sudo LD_LIBRARY_PATH=$LD_LIBRARY_PATH ./sensor_nodeh
# sudo env LD_LIBRARY_PATH=/opt/ros/foxy/lib 

#mq2
echo 109 | sudo tee /sys/class/gpio/export > /dev/null
echo in  | sudo tee /sys/class/gpio/gpio109/direction
#led
echo 101 | sudo tee /sys/class/gpio/export > /dev/null
echo out  | sudo tee /sys/class/gpio/gpio101/direction
sudo chmod 666 /sys/class/gpio/gpio101/value

echo 97 | sudo tee /sys/class/gpio/export > /dev/null
echo out  | sudo tee /sys/class/gpio/gpio97/direction
sudo chmod 666 /sys/class/gpio/gpio97/value

./sensor_node
# wait


