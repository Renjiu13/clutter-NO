## 介绍

此文件为我的个人局域网服务器报告本机的IP地址使用

## 使用PushPlus


```
#!/bin/bash  

  

# PushPlus token  

PUSHPLUS_TOKEN="048f*5912a91*cecbdfga76*28sf4be8cd0a"  

  

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
```



## 使用钉钉机器人

 依赖工具
    
    - 需要安装 `openssl`
    - 建议安装 `jq`（用于URL编码，可选）

```
#!/bin/bash  

# 钉钉机器人 Webhook URL  
DINGTALK_URL="https://oapi.dingtalk.com/robot/send?access_token=d1608cdb218267b4070**fgfasg**156ff17891cddghb2c135ff7b9a"

# 钉钉机器人加签密钥  
SIGNATURE_SECRET="SEC0a1dshjs0516b4f77f580e70011sdghec1905b91232647b997fc8dd"

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

# 钉钉机器人消息格式
DATA=$(cat <<EOF
{
  "msgtype": "text",
  "text": {
    "content": "$MESSAGE"
  },
  "at": {
    "isAtAll": false
  }
}
EOF
)

# 生成签名（正确的HMAC-SHA256+Base64方法）
timestamp=$(date +%s%3N)  # 使用毫秒级时间戳
string_to_sign="$timestamp"$'\n'"$SIGNATURE_SECRET"

# 使用openssl生成签名
sign=$(echo -n "$string_to_sign" | openssl dgst -sha256 -hmac "$SIGNATURE_SECRET" -binary | base64)

# URL编码签名（可选，但建议）
sign=$(printf '%s' "$sign" | jq -sRr @uri)

# 发送通知
RESPONSE=$(curl -s -X POST "$DINGTALK_URL&timestamp=$timestamp&sign=$sign" \
     -H "Content-Type: application/json" \
     -d "$DATA")  

# 输出响应内容，帮助诊断问题
echo "钉钉返回响应：$RESPONSE"

# 检查发送状态  
if [[ "$RESPONSE" == *"\"errcode\":0"* ]]; then  
    echo "通知发送成功"  
else  
    echo "发送通知失败: $RESPONSE"  
fi

```


## 使用飞书机器人

```
#!/bin/bash  
  
# 飞书机器人 Webhook URL  
FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/e929694e-10e9-4947-8b29-2b956cb63f13"  
  
# 获取主机名称  
HOSTNAME=$(hostname)  
  
# 获取当前IPv4地址  
IPV4=$(curl -s myip.ipip.net | awk -F '：| ' '{print $3}')  
  
# 获取当前IPv6地址  
IPV6=$(curl -s -6 icanhazip.com)  
  
# 获取局域网IP地址  
LOCAL_IP=$(ip addr show | grep "inet " | grep -v "127.0.0.1" | awk '{print $2}' | head -n 1)  
  
# 获取问候语  
GREETING=$(curl -s https://v1.hitokoto.cn/ | jq -r '.hitokoto')  
  
# 消息内容  
MESSAGE="设备名称：$HOSTNAME\n\n阿旺您好！\n\n您的IPv4地址：$IPV4\n您的IPv6地址：$IPV6\n您局域网地址：$LOCAL_IP\n\n----------------------\n$GREETING"  
  
# 发送通知到飞书机器人  
curl -s -X POST $FEISHU_WEBHOOK \  
     -H "Content-Type: application/json" \  
     -d '{  
           "msg_type": "text",  
           "content": {  
             "text": "'"$MESSAGE"'"  
           }  
         }'  
  
echo "通知已发送。"
```