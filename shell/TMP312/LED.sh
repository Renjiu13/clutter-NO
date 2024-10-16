#!/bin/bash

# 定义LED控制路径
LED_PATH="/sys/class/leds/red:power/brightness"

# 检查文件是否存在
if [ ! -f "$LED_PATH" ]; then
    echo -e "\033[31mLED控制路径不存在: $LED_PATH\033[0m"
    exit 1
fi

# 获取当前的LED状态
current_state=$(cat "$LED_PATH")

# 提示用户操作
while true; do
    echo -e "\n\033[1;34m============================"
    echo -e "  LED 控制菜单"
    echo -e "============================\033[0m"

    # 根据状态显示不同颜色的状态提示
    if [ "$current_state" -eq 1 ]; then
        echo -e "\033[1;32mLED当前状态：开 (on)\033[0m"
    else
        echo -e "\033[1;31mLED当前状态：关 (off)\033[0m"
    fi

    echo -e "\n\033[1;33m请选择操作：\033[0m"
    echo -e "  打开LED：\033[1;32m1\033[0m"
    echo -e "  关闭LED：\033[1;31m2\033[0m"
    echo -e "  \033[1;37m回车键\033[0m - 退出"
    
    # 读取用户输入
    read -n 1 -r input

    # 如果用户按回车键，退出脚本
    if [ -z "$input" ]; then
        echo -e "\n\033[1;37m退出脚本。\033[0m"
        break
    fi

    case $input in
        1)
            if [ "$current_state" -eq 1 ]; then
                echo -e "\n\033[1;33mLED已经是开状态。\033[0m"
            else
                echo -e "\n\033[1;32m打开LED...\033[0m"
                echo 1 > "$LED_PATH"
                current_state=1
            fi
            ;;
        2)
            if [ "$current_state" -eq 0 ]; then
                echo -e "\n\033[1;33mLED已经是关状态。\033[0m"
            else
                echo -e "\n\033[1;31m关闭LED...\033[0m"
                echo 0 > "$LED_PATH"
                current_state=0
            fi
            ;;
        *)
            echo -e "\n\033[31m无效输入，请按 '1' 打开LED，按 '2' 关闭LED，或按回车键退出。\033[0m"
            ;;
    esac
done

