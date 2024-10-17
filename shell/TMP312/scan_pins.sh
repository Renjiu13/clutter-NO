#!/bin/bash

# 获取脚本所在目录
SCRIPT_DIR="$(dirname "$(realpath "$0")")"

# 日志文件路径
LOG_FILE="$SCRIPT_DIR/gpio_scan.log"

# 清空日志文件
> "$LOG_FILE"

# 函数：记录日志
log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# 函数：检查SSH连接状态
check_ssh_connection() {
    if ! ping -c 1 -W 1 localhost &> /dev/null; then
        return 1  # SSH连接中断
    else
        return 0  # SSH连接正常
    fi
}

# 函数：尝试恢复网络连接
recover_network() {
    log "尝试恢复网络连接"
    
    # 重启网络服务
    sudo systemctl restart networking
    log "重启网络服务"
    
    # 获取当前活动的网络接口
    active_interface=$(ip route | grep default | awk '{print $5}')
    if [ -n "$active_interface" ]; then
        # 重启网络接口
        sudo ip link set dev $active_interface down
        sudo ip link set dev $active_interface up
        log "重启网络接口 $active_interface"
    else
        log "未找到活动的网络接口"
    fi
    
    # 等待几秒钟让网络稳定
    sleep 10
}

# 函数：尝试重新建立SSH连接
reconnect_ssh() {
    log "尝试重新建立SSH连接"
    while ! check_ssh_connection; do
        recover_network
        sleep 5  # 等待5秒后重试
        log "再次尝试连接SSH"
    done
    log "SSH连接已恢复"
}

# 遍历从1到159的所有GPIO引脚
for ii in {1..159}
do
    log "开始测试GPIO引脚: $ii"
    
    # 导出 GPIO 引脚
    echo $ii >/sys/class/gpio/export
    log "导出GPIO引脚: $ii"
    
    # 设置为输出模式
    echo out >/sys/class/gpio/gpio$ii/direction
    log "设置GPIO引脚: $ii 为输出模式"
    
    # 记录原始状态
    original_value=$(cat /sys/class/gpio/gpio$ii/value)
    log "记录GPIO引脚: $ii 的原始状态: $original_value"
    
    # 设置为低电平
    echo 0 >/sys/class/gpio/gpio$ii/value
    log "设置GPIO引脚: $ii 为低电平"
    sleep 1
    
    # 检查SSH连接状态
    if ! check_ssh_connection; then
        log "检测到SSH连接中断，当前GPIO引脚: $ii 可能是网络接口使用的引脚"
        
        # 恢复原始状态
        echo $original_value >/sys/class/gpio/gpio$ii/value
        log "恢复GPIO引脚: $ii 的原始状态: $original_value"
        
        # 尝试恢复网络连接
        recover_network
        
        # 尝试重新建立SSH连接
        reconnect_ssh
        
        # 从日志中提取网络接口使用的GPIO引脚
        net_gpio_pins=$(grep "检测到SSH连接中断" "$LOG_FILE" | awk '{print $10}')
        log "检测到网络接口使用的GPIO引脚: $net_gpio_pins"
        
        # 重启设备
        log "重启设备以恢复网络连接"
        sudo reboot
    fi
    
    # 设置为高电平
    echo 1 >/sys/class/gpio/gpio$ii/value
    log "设置GPIO引脚: $ii 为高电平"
    sleep 1
    
    # 检查SSH连接状态
    if ! check_ssh_connection; then
        log "检测到SSH连接中断，当前GPIO引脚: $ii 可能是网络接口使用的引脚"
        
        # 恢复原始状态
        echo $original_value >/sys/class/gpio/gpio$ii/value
        log "恢复GPIO引脚: $ii 的原始状态: $original_value"
        
        # 尝试恢复网络连接
        recover_network
        
        # 尝试重新建立SSH连接
        reconnect_ssh
        
        # 从日志中提取网络接口使用的GPIO引脚
        net_gpio_pins=$(grep "检测到SSH连接中断" "$LOG_FILE" | awk '{print $10}')
        log "检测到网络接口使用的GPIO引脚: $net_gpio_pins"
        
        # 重启设备
        log "重启设备以恢复网络连接"
        sudo reboot
    fi
    
    # 恢复原始状态
    echo $original_value >/sys/class/gpio/gpio$ii/value
    log "恢复GPIO引脚: $ii 的原始状态: $original_value"
    sleep 3
done

# 从日志中提取网络接口使用的GPIO引脚
net_gpio_pins=$(grep "检测到SSH连接中断" "$LOG_FILE" | awk '{print $10}')
if [ -z "$net_gpio_pins" ]; then
    log "未检测到网络接口使用的GPIO引脚"
else
    log "检测到网络接口使用的GPIO引脚: $net_gpio_pins"
fi