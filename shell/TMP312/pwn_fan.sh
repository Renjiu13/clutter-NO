#!/bin/sh
# 本脚本由 https://LaJiLao.Top 提供

# 获取脚本名称，去掉路径部分
myname="${0##*/}"

# 尝试从 /var/run 目录中读取存储的 PID 文件
temp_pid="$(cat /var/run/${myname}.pid 2>/dev/null)"

# 从 /proc 目录中获取与 PID 关联的进程名称
get_name="$(cat /proc/$temp_pid/comm 2>/dev/null)"

# 生成一个随机数，用于随机延迟
rands=$(awk '{ee==gsub(/[^0-9]/,"");print substr($ee,1,6)}' /proc/sys/kernel/random/uuid)

# 使用 busybox 的 usleep 命令来延迟执行，延迟时间为生成的随机数
busybox usleep $rands

# 如果进程名称与当前脚本名称相同，说明脚本已经在运行，避免重复执行
[ "$get_name" = "$myname" ] && {
    echo "脚本已经执行，请勿重复执行……"
    exit 0
}

{
    # 尝试获取脚本的 PID 并存储在 /var/run 目录下的文件中
    pidof $myname >/var/run/${myname}.pid || pgrep $myname >/var/run/${myname}.pid

    # 定义 GPIO 引脚号，可能用于控制风扇
    ii=152 # 在 tpm312 板子的 minipci 旁边的 4pin 座 (J8917)
    
    # 导出 GPIO 引脚
    echo $ii >/sys/class/gpio/export
    
    # 设置 GPIO 引脚方向为输出
    echo out >/sys/class/gpio/gpio$ii/direction
    
    # 定义 GPIO 引脚的值文件路径
    g_p=/sys/class/gpio/gpio$ii/value

    # 判断 hwmon 目录下的温度文件是否存在，若存在则定义 tempfile 变量指向该文件
    [ -r /sys/class/hwmon/hwmon0/temp1_input ] && tempfile="/sys/class/hwmon/hwmon0/temp1_input" || {
        # 如果 hwmon 文件不存在，则使用 thermal 目录下的温度文件
        [ -r /sys/class/thermal/thermal_zone0/temp ] && tempfile="/sys/class/thermal/thermal_zone0/temp"
    }

    # 定义获取 CPU 温度的函数 get_dw
    get_dw() {
        # 读取 CPU 温度
        cpu_temp=$(cat $tempfile)
        
        # 如果未能读取到 CPU 温度，返回状态码 4
        [ "$cpu_temp" = "" ] && return 4
        
        # 如果 CPU 温度小于等于 45000 毫度 (45°C)
        [ "$cpu_temp" -le "45000" ] && {
            # 如果温度上升到 43000 毫度 (43°C)，返回状态码 1，表示温度升高需要控制
            [ "$pp" = "a" -a "$cpu_temp" -ge "43000" ] && return 1 || {
                pp="" # 否则清空标志
                return 9 # 返回状态码 9，表示温度正常，不需要风扇
            }
        } || {
            # 如果温度在 45000 毫度到 48000 毫度之间，返回状态码 1
            [ "$cpu_temp" -le "48000" -a "$cpu_temp" -gt "45000" ] && return 1 || {
                # 如果温度在 48000 毫度到 51000 毫度之间，返回状态码 2
                [ "$cpu_temp" -le "51000" -a "$cpu_temp" -gt "48000" ] && return 2 || {
                    # 如果温度在 51000 毫度到 55000 毫度之间，返回状态码 3
                    [ "$cpu_temp" -le "55000" -a "$cpu_temp" -gt "51000" ] && return 3 || return 4
                }
            }
        }
    }

    # 定义设置风扇 PWM 输出的函数 set_wd，参数为高电平和低电平的持续时间
    set_wd() {
        # 设置 GPIO 输出为高电平
        echo 1 >$g_p
        busybox usleep $1 # 持续高电平时间
        # 设置 GPIO 输出为低电平
        echo 0 >$g_p
        busybox usleep $2 # 持续低电平时间
    }

    # 无限循环，根据 CPU 温度控制风扇 PWM
    while :
    do
        # 调用获取 CPU 温度函数
        get_dw
        # 根据函数返回值执行不同的风扇控制逻辑
        case $? in
            9)
                echo 0 >$g_p # 温度正常，风扇关闭
                sleep 1 # 等待 1 秒
                ;;
            1)
                pp=a
                set_wd 2500 250 # 温度较高时设置 PWM 占空比
                ;;
            2)
                pp=a
                set_wd 10000 500 # 温度升高时调整 PWM 占空比
                ;;
            3)
                pp=a
                set_wd 15000 300 # 温度更高时进一步调整 PWM 占空比
                ;;
            4)
                pp=a
                set_wd 20000 100 # 温度非常高时保持较长的高电平，风扇全速运行
                echo 1 >$g_p # 始终保持风扇运行
                sleep 1 # 等待 1 秒
                ;;
        esac
    done
} >/dev/null 2>&1 & # 将脚本的所有输出重定向到 /dev/null
