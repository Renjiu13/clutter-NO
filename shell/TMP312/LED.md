## 关于TMP312灯光控制脚本教程

在Linux系统中，控制LED灯的开关通常涉及到对 `/sys/class/leds` 目录下的文件进行操作。以下是一个简单的步骤指南，帮助你控制LED灯。

首先，打开终端输入

```
ls /sys/class/leds/
```
可以看到一下内容

```
root@tpm312:/home/shell# ls /sys/class/leds/
mmc0::  red:pwr_led
```

查看LED状态
```
cat /sys/class/leds/red:pwr_led/brightness
```

要打开LED，请执行以下命令：
```
echo 0 | sudo tee /sys/class/leds/red:pwr_led/brightness
```

要关闭LED，请执行以下命令：
```
echo 1 | sudo tee /sys/class/leds/red:pwr_led/brightness
```
## 全局使用led命令

创建脚本文件
```
sudo nano /usr/local/bin/led
```

赋予脚本执行权限
```
sudo chmod +x /usr/local/bin/led
```
或者创建符号链接
```
ln -s /usr/local/bin/led /home/shell/led
```
运行脚本
```
led
```



#### 脚本示例
```
#!/bin/bash

# 定义LED控制路径
LED_PATH="/sys/class/leds/red:pwr_led/brightness"

# 检查文件是否存在
if [ ! -f "$LED_PATH" ]; then 
    echo -e "\033[31mLED控制路径不存在: $LED_PATH\033[0m"
    exit 1
fi

# 获取当前LED状态
current_state=$(cat "$LED_PATH")

# 定义函数来打开LED
start_led() {
    echo "打开 LED..."
    echo 0 | sudo tee "$LED_PATH" > /dev/null
}

# 定义函数来关闭LED
stop_led() {
    echo "关闭 LED..."
    echo 1 | sudo tee "$LED_PATH" > /dev/null
}

# 根据当前状态切换LED
if [ "$current_state" -eq 0 ]; then
    stop_led
else
    start_led
fi
```
