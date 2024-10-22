#!/bin/bash

# Docker 源地址
MIRRORS=(
  "https://docker.1ms.run"
  "https://hub.rat.dev"
  "https://docker.1panel.live"
  "https://docker.m.daocloud.io"
  "https://dockerproxy.net"
)

# Docker 配置文件路径
DOCKER_CONFIG_FILE="/etc/docker/daemon.json"

# 检查 Docker 配置文件是否存在
if [ ! -f "$DOCKER_CONFIG_FILE" ]; then
  echo "Docker 配置文件不存在，创建一个新的配置文件..."
  sudo touch "$DOCKER_CONFIG_FILE"
fi

# 写入 Docker 源地址到配置文件
echo "{
  \"registry-mirrors\": [
    $(for mirror in "${MIRRORS[@]}"; do echo "\"$mirror\""; done)
  ]
}" | sudo tee "$DOCKER_CONFIG_FILE" > /dev/null

# 重启 Docker 服务
sudo systemctl restart docker

echo "Docker 源地址更换成功！"
