#!/bin/bash

for ii in {1..159}
do
    echo $ii >/sys/class/gpio/export  # 导出 GPIO 引脚
    echo out >/sys/class/gpio/gpio$ii/direction  # 设置为输出模式
    echo 0 >/sys/class/gpio/gpio$ii/value  # 设置为低电平
    sleep 1  # 等待 1 秒
    echo 1 >/sys/class/gpio/gpio$ii/value  # 设置为高电平
    read -s -n1 -p "当前gpio是：$ii，按任意键继续 ... "  # 等待用户输入
    echo ""
done