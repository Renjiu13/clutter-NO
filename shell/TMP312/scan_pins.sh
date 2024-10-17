#!/bin/bash

# 获取脚本所在目录
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
LOG_FILE="$SCRIPT_DIR/gpio_scan.log"

# 清空日志文件
> "$LOG_FILE"

# 可配置参数
START_PIN=1
END_PIN=159
RETRY_INTERVAL=5
NETWORK_WAIT_TIME=10

# 函数：记录日志
log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# 函数：检查SSH连接状态
check_ssh_connection() {
    ping -c 1 -W 1 localhost &> /dev/null
}

# 函数：尝试恢复网络连接
recover_network() {
    log "尝试恢复网络连接"
    if ! sudo systemctl restart networking; then
        log "重启网络服务失败"
    else
        log "重启网络服务成功"
    fi

    active_interface=$(ip route | grep default | awk '{print $5}')
    if [ -n "$active_interface" ]; then
        sudo ip link set dev "$active_interface" down
        sudo ip link set dev "$active_interface" up
        log "重启网络接口 $active_interface"
    else
        log "未找到活动的网络接口"
    fi
    
    sleep "$NETWORK_WAIT_TIME"
}

# 函数：尝试重新建立SSH连接
reconnect_ssh() {
    log "尝试重新建立SSH连接"
    while ! check_ssh_connection; do
        recover_network
        sleep "$RETRY_INTERVAL"
        log "再次尝试连接SSH"
    done
    log "SSH连接已恢复"
}

# 记录网络接口使用的GPIO引脚
net_gpio_pins=""

# 遍历GPIO引脚
for ii in $(seq "$START_PIN" "$END_PIN")
do
    log "开始测试GPIO引脚: $ii"
    echo "$ii" >/sys/class/gpio/export
    echo out >/sys/class/gpio/gpio"$ii"/direction
    
    original_value=$(cat /sys/class/gpio/gpio"$ii"/value)
    log "记录GPIO引脚: $ii 的原始状态: $original_value"

    for value in 0 1; do
        echo "$value" >/sys/class/gpio/gpio"$ii"/value
        log "设置GPIO引脚: $ii 为 ${value}电平"
        sleep 1

        if ! check_ssh_connection; then
            log "检测到SSH连接中断，当前GPIO引脚: $ii 可能是网络接口使用的引脚"
            echo "$original_value" >/sys/class/gpio/gpio"$ii"/value
            log "恢复GPIO引脚: $ii 的原始状态: $original_value"
            
            recover_network
            reconnect_ssh

            net_gpio_pins+="$ii "
            log "记录网络接口使用的GPIO引脚: $ii"
            break
        fi
    done
    
    # 恢复原始状态
    echo "$original_value" >/sys/class/gpio/gpio"$ii"/value
    log "恢复GPIO引脚: $ii 的原始状态: $original_value"
    sleep 3
done

# 日志总结
if [ -z "$net_gpio_pins" ]; then
    log "未检测到网络接口使用的GPIO引脚"
else
    log "检测到网络接口使用的GPIO引脚: $net_gpio_pins"
fi

# 最后重启设备
log "重启设备以恢复网络连接"
sudo reboot
