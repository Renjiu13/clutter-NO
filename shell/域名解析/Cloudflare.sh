#!/bin/bash

# 配置信息
CF_API_TOKEN="你的Cloudflare令牌"      # 替换为你的Cloudflare API令牌
CF_DOMAIN="confused.us.kg"             # 你的主域名
CF_SUBDOMAIN="an.confused.us.kg"       # 需要更新的完整域名

# 功能开关
ENABLE_IPV6=true                       # 是否启用IPv6更新
ENABLE_NOTIFICATIONS=true              # 是否启用通知功能
PUSHPLUS_TOKEN="048f05912a914cecba7642804be8cd0a"  # 你的PushPlus推送令牌

# 重试配置
MAX_RETRIES=3                          # 最大重试次数
RETRY_INTERVAL=5                       # 重试间隔（秒）

# 发送通知的函数
send_notification() {
    if [ "$ENABLE_NOTIFICATIONS" != true ]; then
        return 0
    fi
    
    local title="$1"
    local content="$2"
    local username=$(whoami)
    local current_time=$(date '+%Y-%m-%d %H:%M:%S')
    
    local detailed_content="⏰ 更新时间：
${current_time}

🌐 更新域名：
${CF_SUBDOMAIN}

👤 执行用户：
${username}

📌 更新详情：
${content}"
    
    local retry_count=0
    while [ $retry_count -lt $MAX_RETRIES ]; do
        response=$(curl -s -w "\n%{http_code}" "http://www.pushplus.plus/send" \
            -H "Content-Type: application/json" \
            -d "{
                \"token\": \"${PUSHPLUS_TOKEN}\",
                \"title\": \"${title}\",
                \"content\": \"${detailed_content}\",
                \"template\": \"markdown\"
            }")
        
        http_code=$(echo "$response" | tail -n1)
        if [ "$http_code" = "200" ]; then
            return 0
        fi
        
        retry_count=$((retry_count + 1))
        [ $retry_count -lt $MAX_RETRIES ] && sleep $RETRY_INTERVAL
    done
    
    echo "警告: 发送通知失败，已重试 $MAX_RETRIES 次"
    return 1
}

# 获取IPv6地址的函数
get_ipv6_address() {
    local retry_count=0
    while [ $retry_count -lt $MAX_RETRIES ]; do
        local ipv6=$(curl -6 -s --max-time 10 http://ifconfig.co)
        if [ ! -z "$ipv6" ]; then
            echo "$ipv6"
            return 0
        fi
        retry_count=$((retry_count + 1))
        [ $retry_count -lt $MAX_RETRIES ] && sleep $RETRY_INTERVAL
    done
    return 1
}

# 获取Cloudflare API响应的函数
get_cloudflare_api() {
    local url="$1"
    local retry_count=0
    
    while [ $retry_count -lt $MAX_RETRIES ]; do
        local response=$(curl -s -X GET "$url" \
            -H "Authorization: Bearer ${CF_API_TOKEN}" \
            -H "Content-Type: application/json")
        
        if [ ! -z "$response" ]; then
            echo "$response"
            return 0
        fi
        
        retry_count=$((retry_count + 1))
        [ $retry_count -lt $MAX_RETRIES ] && sleep $RETRY_INTERVAL
    done
    return 1
}

# 主要逻辑
if [ "$ENABLE_IPV6" = true ]; then
    current_ipv6_address=$(get_ipv6_address)
    if [ -z "$current_ipv6_address" ]; then
        send_notification "🔴 DDNS更新失败" "无法获取IPv6地址（已重试 $MAX_RETRIES 次）"
        echo "错误: 无法获取IPv6地址"
        exit 1
    fi
    echo "当前IPv6地址: ${current_ipv6_address}"
    
    # 获取Zone ID
    zone_response=$(get_cloudflare_api "https://api.cloudflare.com/client/v4/zones?name=${CF_DOMAIN}")
    zone_id=$(echo "$zone_response" | jq -r '.result[0].id')
    
    if [ -z "$zone_id" ] || [ "$zone_id" = "null" ]; then
        send_notification "🔴 DDNS更新失败" "无法获取Zone ID"
        echo "错误: 无法获取Zone ID"
        exit 1
    fi
    echo "Zone ID: ${zone_id}"
    
    # 获取Record ID
    record_response=$(get_cloudflare_api "https://api.cloudflare.com/client/v4/zones/${zone_id}/dns_records?type=AAAA&name=${CF_SUBDOMAIN}")
    record_id=$(echo "$record_response" | jq -r '.result[0].id')
    
    if [ -z "$record_id" ] || [ "$record_id" = "null" ]; then
        send_notification "🔴 DDNS更新失败" "无法获取Record ID"
        echo "错误: 无法获取Record ID"
        exit 1
    fi
    echo "Record ID: ${record_id}"
    
    # 获取当前DNS记录
    current_record_response=$(get_cloudflare_api "https://api.cloudflare.com/client/v4/zones/${zone_id}/dns_records/${record_id}")
    current_record_ipv6=$(echo "$current_record_response" | jq -r '.result.content')
    
    # 需要时更新DNS记录
    if [ "$current_ipv6_address" != "$current_record_ipv6" ]; then
        retry_count=0
        while [ $retry_count -lt $MAX_RETRIES ]; do
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
                exit 0
            fi
            
            retry_count=$((retry_count + 1))
            [ $retry_count -lt $MAX_RETRIES ] && sleep $RETRY_INTERVAL
        done
        
        message="❌ 更新状态：失败（已重试 $MAX_RETRIES 次）

📍 当前IPv6地址：
${current_ipv6_address}

❗ 错误信息：
${update_response}"
        send_notification "🔴 DDNS更新失败" "$message"
        echo "$message"
        exit 1
    else
        echo "IPv6地址未发生变化，无需更新"
        if [ "$ENABLE_NOTIFICATIONS" = true ]; then
            message="📍 当前IPv6地址：
${current_ipv6_address}

ℹ️ 状态：无需更新"
            send_notification "📌 DDNS检查" "$message"
        fi
    fi
else
    echo "IPv6更新功能已禁用"
fi