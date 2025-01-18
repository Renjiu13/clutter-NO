#!/bin/bash

# 安装jq工具，用于解析JSON数据
# pkg install jq -y

# 配置信息
# 替换为你的Cloudflare API令牌
CF_API_TOKEN="你的Cloudflare令牌"  

# 你的主域名    
CF_DOMAIN="baudu.com" 

# 需要更新的完整域名            
CF_SUBDOMAIN="an.baudu.com" 

 # 你的PushPlus推送令牌      
PUSHPLUS_TOKEN="048f05912239*32465642803df*格式cd0a" 

# 发送通知的函数
send_notification() {
    local title="$1"
    local content="$2"
    local username=$(whoami)
    local current_time=$(date '+%Y-%m-%d %H:%M:%S')
    
    # 构建适合手机查看的消息内容
    local detailed_content="📝 DDNS更新通知
------------------
⏰ 更新时间：
${current_time}

🌐 更新域名：
${CF_SUBDOMAIN}

👤 执行用户：
${username}

📌 更新详情：
${content}"
    
    # 发送到PushPlus
    curl -s "http://www.pushplus.plus/send" \
        -H "Content-Type: application/json" \
        -d "{
            \"token\": \"${PUSHPLUS_TOKEN}\",
            \"title\": \"${title}\",
            \"content\": \"${detailed_content}\",
            \"template\": \"markdown\"
        }"
}

# 获取当前IPv6地址
current_ipv6_address=$(curl -6 -s http://ifconfig.co)
if [ -z "$current_ipv6_address" ]; then
    send_notification "🔴 DDNS更新失败" "无法获取IPv6地址"
    echo "错误: 无法获取IPv6地址"
    exit 1
fi
echo "当前IPv6地址: ${current_ipv6_address}"

# 获取Zone ID
zone_id=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones?name=${CF_DOMAIN}" \
    -H "Authorization: Bearer ${CF_API_TOKEN}" \
    -H "Content-Type: application/json" | jq -r '.result[0].id')

if [ -z "$zone_id" ] || [ "$zone_id" = "null" ]; then
    send_notification "🔴 DDNS更新失败" "无法获取Zone ID"
    echo "错误: 无法获取Zone ID"
    exit 1
fi
echo "Zone ID: ${zone_id}"

# 获取Record ID
record_id=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/${zone_id}/dns_records?type=AAAA&name=${CF_SUBDOMAIN}" \
    -H "Authorization: Bearer ${CF_API_TOKEN}" \
    -H "Content-Type: application/json" | jq -r '.result[0].id')

if [ -z "$record_id" ] || [ "$record_id" = "null" ]; then
    send_notification "🔴 DDNS更新失败" "无法获取Record ID"
    echo "错误: 无法获取Record ID"
    exit 1
fi
echo "Record ID: ${record_id}"

# 获取当前DNS记录
current_record_ipv6=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/${zone_id}/dns_records/${record_id}" \
    -H "Authorization: Bearer ${CF_API_TOKEN}" \
    -H "Content-Type: application/json" | jq -r '.result.content')

# 需要时更新DNS记录
if [ "$current_ipv6_address" != "$current_record_ipv6" ]; then
    update_response=$(curl -s -X PUT "https://api.cloudflare.com/client/v4/zones/${zone_id}/dns_records/${record_id}" \
        -H "Authorization: Bearer ${CF_API_TOKEN}" \
        -H "Content-Type: application/json" \
        --data "{
            \"type\": \"AAAA\",
            \"name\": \"${CF_SUBDOMAIN}\",
            \"content\": \"${current_ipv6_address}\",
            \"ttl\": 120,
            \"proxied\": false
        }")
    
    if echo "$update_response" | grep -q "\"success\":true"; then
        message="✅ 更新状态：成功

📍 旧IPv6地址：
${current_record_ipv6}

📍 新IPv6地址：
${current_ipv6_address}"
        send_notification "🟢 DDNS更新成功" "$message"
        echo "$message"
    else
        message="❌ 更新状态：失败

📍 当前IPv6地址：
${current_ipv6_address}

❗ 错误信息：
${update_response}"
        send_notification "🔴 DDNS更新失败" "$message"
        echo "$message"
    fi
else
    echo "IPv6地址未发生变化，无需更新"
    # 可选的未变化通知
    # message="📍 当前IPv6地址：
    # ${current_ipv6_address}
    #
    # ℹ️ 状态：无需更新"
    # send_notification "📌 DDNS检查" "$message"
fi