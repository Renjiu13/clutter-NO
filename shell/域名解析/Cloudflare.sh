#!/bin/bash

# 安装jq工具，用于解析JSON数据
# pkg install jq -y

# Cloudflare API配置
# 请确保替换以下变量的实际值：
#   CF_API_TOKEN: Cloudflare API令牌
#   CF_DOMAIN: 主域名
#   CF_SUBDOMAIN: 目标子域名
CF_API_TOKEN="MQT_Jd4HlZExfWeU8GETgsM5NinKf4d"
CF_DOMAIN="roe.top"
CF_SUBDOMAIN="wifi.r.top"

# 获取当前的公网IPv6地址
# 优先从网卡获取IPv6公网地址
current_ipv6_address=$(ip -6 addr show | grep -oP '(?<=inet6\s)[^ ]+%' | grep -v fe80 | head -n 1)

# 如果从网卡获取不到IPv6地址，则使用curl命令获取
if [ -z "$current_ipv6_address" ]; then
    current_ipv6_address=$(curl -6 -s http://ifconfig.co)
fi

# 检查是否成功获取IPv6地址
if [ -z "$current_ipv6_address" ]; then
    echo "Failed to retrieve IPv6 address"
    exit 1
else
    echo "Successfully retrieved IPv6 address: ${current_ipv6_address}"
fi

# 获取Zone ID
# 通过Cloudflare API获取与主域名关联的Zone ID
zone_id=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones?name=${CF_DOMAIN}" \
    -H "Authorization: Bearer ${CF_API_TOKEN}" \
    -H "Content-Type: application/json" | jq -r '.result[0].id')

if [ -z "$zone_id" ]; then
    echo "Failed to retrieve Zone ID"
    exit 1
else
    echo "Successfully retrieved Zone ID: ${zone_id}"
fi

# 获取Record ID
# 通过Cloudflare API获取子域名的DNS记录ID
record_id=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/${zone_id}/dns_records?type=AAAA&name=${CF_SUBDOMAIN}" \
    -H "Authorization: Bearer ${CF_API_TOKEN}" \
    -H "Content-Type: application/json" | jq -r '.result[0].id')

if [ -z "$record_id" ]; then
    echo "Failed to retrieve Record ID"
    exit 1
else
    echo "Successfully retrieved Record ID: ${record_id}"
fi

# 获取当前Cloudflare记录中的IPv6地址
# 通过Cloudflare API获取子域名当前的AAAA记录内容（IPv6地址）
current_record_ipv6=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/${zone_id}/dns_records/${record_id}" \
    -H "Authorization: Bearer ${CF_API_TOKEN}" \
    -H "Content-Type: application/json" | jq -r '.result.content')

# 检查当前的IPv6地址是否与Cloudflare记录中的IPv6地址不同
if [ "$current_ipv6_address" != "$current_record_ipv6" ]; then
    # 更新Cloudflare上的IPv6地址
    # 通过Cloudflare API更新子域名的AAAA记录内容
    update_response=$(curl -s -X PUT "https://api.cloudflare.com/client/v4/zones/${zone_id}/dns_records/${record_id}" \
        -H "Authorization: Bearer ${CF_API_TOKEN}" \
        -H "Content-Type: application/json" \
        --data "{\"type\":\"AAAA\",\"name\":\"${CF_SUBDOMAIN}\",\"content\":\"${current_ipv6_address}\",\"ttl\":120,\"proxied\":false}")

    # 检查更新是否成功
    if echo "$update_response" | grep -q "\"success\":true"; then
        echo "IPv6 地址更新成功: ${current_ipv6_address}"
    else
        echo "IPv6 地址更新失败: $update_response"
    fi
else
    echo "IPv6 地址没有变化。"
fi
