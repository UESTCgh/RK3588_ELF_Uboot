#!/bin/bash
echo 449 | sudo tee /sys/class/gpio/export
sleep 0.1
echo in | sudo tee /sys/class/gpio/gpio449/direction
sudo chmod 444 /sys/class/gpio/gpio449/value

