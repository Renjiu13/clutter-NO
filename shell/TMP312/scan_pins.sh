#!/bin/bash

# 获取网络接口使用的GPIO引脚列表
# 假设这些是网络接口使用的GPIO引脚
net_gpio_pins=(4 5 6)  

# 遍历从1到159的所有GPIO引脚
for ii in {1..159}
do
    # 跳过网络接口使用的GPIO引脚
    if [[ " ${net_gpio_pins[@]} " =~ " ${ii} " ]]; then
        echo "跳过GPIO引脚: $ii"  # 输出跳过的GPIO引脚信息
        continue  # 跳过当前循环
    fi

    # 导出 GPIO 引脚
    echo $ii >/sys/class/gpio/export
    # 设置为输出模式
    echo out >/sys/class/gpio/gpio$ii/direction
    # 记录原始状态
    original_value=$(cat /sys/class/gpio/gpio$ii/value)  # 读取并记录当前GPIO引脚的原始状态
    # 设置为低电平
    echo 0 >/sys/class/gpio/gpio$ii/value
    sleep 1  # 等待 1 秒
    # 设置为高电平
    echo 1 >/sys/class/gpio/gpio$ii/value
    read -s -n1 -p "当前gpio是：$ii，按任意键继续 ... "  # 等待用户输入
    echo ""  # 换行

    # 恢复原始状态
    echo $original_value >/sys/class/gpio/gpio$ii/value  # 恢复GPIO引脚的原始状态
    sleep 3  # 等待 3 秒
done