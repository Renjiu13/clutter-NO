#!/bin/bash  

# PushPlus token  
PUSHPLUS_TOKEN="048f*5912a91*cecba76*28sf4be8cd0a"  

# 获取当前IPv4地址，超时4秒  
IPV4=$(timeout 4s curl -s myip.ipip.net | awk -F '：| ' '{print $3}') || IPV4="获取IPv4地址超时"  

# 获取当前IPv6地址，超时4秒  
IPV6=$(timeout 4s curl -s -6 icanhazip.com) || IPV6="获取IPv6地址超时"  

# 获取局域网IP地址  
LOCAL_IP=$(ip addr show | grep "inet " | grep -v "127.0.0.1" | awk '{print $2}' | head -n 1)  
[ -z "$LOCAL_IP" ] && LOCAL_IP="无法获取局域网IP地址"  

# 获取温度数值，超时4秒  
TEMPERATURES=$(timeout 4s sensors | grep 'temp1' | awk '{print $2}' | sed 's/[^+]*\+//')  
[ -z "$TEMPERATURES" ] && TEMPERATURES="获取温度超时或失败"  

# 如果有多个温度值，提取第一个温度
TEMPERATURE=$(echo "$TEMPERATURES" | head -n 1 | sed 's/°C//')

# 获取问候语，超时4秒  
GREETING=$(timeout 4s curl -s https://api.ahfi.cn/api/getGreetingMessage) || GREETING="获取问候语超时"  

# 消息内容  
MESSAGE=$(cat <<EOF
阿旺您好！

您的IPv4地址：$IPV4
您的IPv6地址：$IPV6
您局域网地址：$LOCAL_IP
您的机器温度：$TEMPERATURE°C

----------------------
$GREETING
EOF
)  

# 发送通知  
RESPONSE=$(curl -s -X POST https://www.pushplus.plus/send \
     -H "Content-Type: application/json" \
     -d '{  
           "token": "'"$PUSHPLUS_TOKEN"'",  
           "title": "IP地址及温度通知",  
           "content": "'"$MESSAGE"'",  
           "template": "html"  
         }')  

# 检查发送状态  
if [ $? -ne 0 ]; then  
    echo "发送通知失败: $RESPONSE"  
else  
    echo "通知已成功发送"  
fi
