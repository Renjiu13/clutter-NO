## 自动脚本一

- **说明**
	- 固定版本为`0.51.3`
	- 

```
#!/bin/bash
# frp 客户端和服务端自动安装脚本
# 支持 ARM 和 AMD 架构
# 支持系统服务控制

# 设置颜色变量
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
PLAIN="\033[0m"

# 初始化变量
init_var(){
    export FRP_VER=0.51.3
    # 识别系统架构
    case "$(uname -m)" in
        x86_64|amd64)
            ARCH="amd64"
            ;;
        armv7l|armv8l|aarch64)
            ARCH="arm64"
            ;;
        *)
            echo -e "${RED}不支持的系统架构！${PLAIN}"
            exit 1
            ;;
    esac
}

# 检查系统
check_sys(){
    if [[ -f /etc/redhat-release ]]; then
        release="centos"
    elif cat /etc/issue | grep -q -E -i "debian"; then
        release="debian"
    elif cat /etc/issue | grep -q -E -i "ubuntu"; then
        release="ubuntu"
    elif cat /etc/issue | grep -q -E -i "centos|red hat|redhat"; then
        release="centos"
    elif cat /proc/version | grep -q -E -i "debian"; then
        release="debian"
    elif cat /proc/version | grep -q -E -i "ubuntu"; then
        release="ubuntu"
    elif cat /proc/version | grep -q -E -i "centos|red hat|redhat"; then
        release="centos"
    fi
}

# 安装依赖
install_depend(){
    if [[ ${release} == "centos" ]]; then
        yum install -y wget tar
    elif [[ ${release} == "debian" || ${release} == "ubuntu" ]]; then
        apt-get update
        apt-get install -y wget tar
    fi
}

# 选择安装类型
choose_type(){
    echo -e "${GREEN}请选择安装类型：${PLAIN}"
    echo -e "${YELLOW}1. 安装 frp 服务端${PLAIN}"
    echo -e "${YELLOW}2. 安装 frp 客户端${PLAIN}"
    read -p "请输入数字 [1-2]：" choose
    case $choose in
        1)
            TYPE="frps"
            ;;
        2)
            TYPE="frpc"
            ;;
        *)
            echo -e "${RED}输入错误，请重新运行脚本！${PLAIN}"
            exit 1
            ;;
    esac
}

# 下载文件
download_files(){
    wget --no-check-certificate -O frp_${FRP_VER}_linux_${ARCH}.tar.gz https://github.com/fatedier/frp/releases/download/v${FRP_VER}/frp_${FRP_VER}_linux_${ARCH}.tar.gz
    tar -zxvf frp_${FRP_VER}_linux_${ARCH}.tar.gz
}

# 配置 frp
config_frp(){
    rm -rf /usr/local/frp
    mkdir -p /usr/local/frp
    cd frp_${FRP_VER}_linux_${ARCH}
    cp ${TYPE} /usr/local/frp/
    mkdir -p /etc/frp
    cp ${TYPE}.ini /etc/frp/
    
    if [ "$TYPE" = "frps" ]; then
        # 配置服务端
        read -p "请输入服务端端口（默认：7000）：" bind_port
        bind_port=${bind_port:-7000}
        read -p "请输入 Dashboard 端口（默认：7500）：" dashboard_port
        dashboard_port=${dashboard_port:-7500}
        read -p "请输入 Dashboard 用户名（默认：admin）：" dashboard_user
        dashboard_user=${dashboard_user:-admin}
        read -p "请输入 Dashboard 密码（默认：admin）：" dashboard_pwd
        dashboard_pwd=${dashboard_pwd:-admin}
        read -p "请输入认证 token（默认：12345678）：" token
        token=${token:-12345678}
        
        cat > /etc/frp/${TYPE}.ini << EOF
[common]
bind_port = ${bind_port}
token = ${token}
dashboard_port = ${dashboard_port}
dashboard_user = ${dashboard_user}
dashboard_pwd = ${dashboard_pwd}
EOF
    else
        # 配置客户端
        read -p "请输入服务器 IP 地址：" server_addr
        read -p "请输入服务器端口（默认：7000）：" server_port
        server_port=${server_port:-7000}
        read -p "请输入认证 token（默认：12345678）：" token
        token=${token:-12345678}
        
        cat > /etc/frp/${TYPE}.ini << EOF
[common]
server_addr = ${server_addr}
server_port = ${server_port}
token = ${token}

[ssh]
type = tcp
local_ip = 127.0.0.1
local_port = 22
remote_port = 6000
EOF
    fi
}

# 配置服务
config_service(){
    cat > /etc/systemd/system/${TYPE}.service << EOF
[Unit]
Description=${TYPE} service
After=network.target syslog.target
Wants=network.target

[Service]
Type=simple
ExecStart=/usr/local/frp/${TYPE} -c /etc/frp/${TYPE}.ini
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl start ${TYPE}
    systemctl enable ${TYPE}
}

# 清理文件
clean_files(){
    rm -rf frp_${FRP_VER}_linux_${ARCH}*
}

# 显示配置信息
show_config(){
    echo -e "${GREEN}=== ${TYPE} 安装完成 ===${PLAIN}"
    echo -e "${GREEN}配置文件：/etc/frp/${TYPE}.ini${PLAIN}"
    echo -e "${GREEN}程序文件：/usr/local/frp/${TYPE}${PLAIN}"
    echo -e "${GREEN}服务启动：systemctl start ${TYPE}${PLAIN}"
    echo -e "${GREEN}服务关闭：systemctl stop ${TYPE}${PLAIN}"
    echo -e "${GREEN}服务重启：systemctl restart ${TYPE}${PLAIN}"
    echo -e "${GREEN}服务状态：systemctl status ${TYPE}${PLAIN}"
    echo -e "${GREEN}安装目录：/usr/local/frp${PLAIN}"
    
    if [ "$TYPE" = "frps" ]; then
        echo -e "${GREEN}Dashboard 地址：http://服务器IP:${dashboard_port}${PLAIN}"
        echo -e "${GREEN}Dashboard 用户名：${dashboard_user}${PLAIN}"
        echo -e "${GREEN}Dashboard 密码：${dashboard_pwd}${PLAIN}"
    fi
}

# 主进程
main(){
    init_var
    check_sys
    install_depend
    choose_type
    download_files
    config_frp
    config_service
    clean_files
    show_config
}

main
```


# 自动脚本二


```
#!/bin/bash

set -e

# 获取最新的 FRP 版本
get_latest_frp_version() {
  echo "正在获取 FRP 最新版本信息..."
  local latest_version=$(curl -s https://api.github.com/repos/fatedier/frp/releases/latest | grep 'tag_name' | cut -d '"' -f 4)
  if [ -z "$latest_version" ]; then
    echo "无法获取 FRP 最新版本信息，请检查网络连接。"
    exit 1
  fi
  echo "$latest_version"
}

# 识别系统架构
get_architecture() {
  local arch=$(uname -m)
  case "$arch" in
    x86_64) echo "amd64" ;;
    aarch64) echo "arm64" ;;
    armv7l) echo "arm" ;;
    *)
      echo "不支持的架构：$arch"
      exit 1
      ;;
  esac
}

# 下载并解压 FRP
install_frp() {
  local version=$1
  local arch=$2
  local frp_type=$3

  echo "准备安装 FRP $frp_type，版本：$version，架构：$arch"

  # 清理旧文件
  echo "清理旧文件..."
  rm -rf /usr/local/frp /tmp/frp_*

  # 下载 FRP 压缩包
  local frp_file="frp_${version}_linux_${arch}.tar.gz"
  local download_url="https://github.com/fatedier/frp/releases/download/${version}/${frp_file}"
  echo "下载 FRP 压缩包：$download_url"
  curl -L -o "/tmp/${frp_file}" "$download_url"

  # 解压并安装
  echo "解压 FRP 压缩包..."
  mkdir -p /usr/local/frp
  tar -zxvf "/tmp/${frp_file}" -C /usr/local/frp --strip-components=1

  # 配置 Systemd
  echo "配置 systemd 服务..."
  local service_file="/etc/systemd/system/frp.service"
  if [ "$frp_type" == "server" ]; then
    cat > "$service_file" <<EOF
[Unit]
Description=FRP Server Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/frp/frps -c /usr/local/frp/frps.ini
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF
  else
    cat > "$service_file" <<EOF
[Unit]
Description=FRP Client Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/frp/frpc -c /usr/local/frp/frpc.ini
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF
  fi

  # 启用并启动服务
  echo "启用并启动 FRP 服务..."
  systemctl daemon-reload
  systemctl enable frp
  systemctl start frp

  echo "FRP $frp_type 安装完成！配置文件位于 /usr/local/frp/"
}

# 检查必需的软件
check_dependencies() {
  echo "检查并安装必需软件..."
  if ! command -v curl &> /dev/null; then
    echo "安装 curl..."
    apt update && apt install -y curl
  fi
}

# 主程序
main() {
  check_dependencies

  local version=$(get_latest_frp_version)
  local arch=$(get_architecture)

  echo "请选择要安装的 FRP 类型："
  echo "1) 客户端"
  echo "2) 服务端"
  read -p "输入数字选择 (1/2): " choice

  case "$choice" in
    1)
      install_frp "$version" "$arch" "client"
      ;;
    2)
      install_frp "$version" "$arch" "server"
      ;;
    *)
      echo "无效选择，退出。"
      exit 1
      ;;
  esac
}

main

```


# 版本三

- **使用Cloud3.5**

```
#!/bin/bash

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 检查是否为root用户
check_root() {
    if [ "$(id -u)" != "0" ]; then
        echo -e "${RED}错误: 此脚本需要root权限运行${NC}"
        exit 1
    fi
}

# 检查并安装必需的软件包
check_dependencies() {
    local dependencies=("curl" "wget" "tar" "jq")
    local need_install=()
    
    for dep in "${dependencies[@]}"; do
        if ! command -v "$dep" >/dev/null 2>&1; then
            need_install+=("$dep")
        fi
    done
    
    if [ ${#need_install[@]} -ne 0 ]; then
        echo -e "${YELLOW}正在安装必需的软件包...${NC}"
        if command -v apt >/dev/null 2>&1; then
            apt update >/dev/null 2>&1
            apt install -y "${need_install[@]}" >/dev/null 2>&1
        elif command -v yum >/dev/null 2>&1; then
            yum install -y epel-release >/dev/null 2>&1
            yum install -y "${need_install[@]}" >/dev/null 2>&1
        else
            echo -e "${RED}不支持的包管理器${NC}"
            exit 1
        fi
    fi
}

# 获取系统架构
get_arch() {
    local arch=$(uname -m)
    case "$arch" in
        x86_64)
            echo "amd64"
            ;;
        aarch64)
            echo "arm64"
            ;;
        armv7l)
            echo "arm"
            ;;
        *)
            echo -e "${RED}不支持的架构: $arch${NC}"
            exit 1
            ;;
    esac
}

# 获取最新版本
get_latest_version() {
    local latest_version=$(curl -s https://api.github.com/repos/fatedier/frp/releases/latest | jq -r .tag_name)
    if [ -z "$latest_version" ]; then
        echo -e "${RED}获取最新版本失败${NC}"
        exit 1
    fi
    echo "$latest_version"
}

# 备份旧文件
backup_old_files() {
    local timestamp=$(date +%Y%m%d_%H%M%S)
    if [ -d "/usr/local/frp" ]; then
        echo -e "${YELLOW}备份旧文件...${NC}"
        tar -czf "/usr/local/frp_backup_$timestamp.tar.gz" /usr/local/frp >/dev/null 2>&1
        rm -rf /usr/local/frp
    fi
}

# 创建服务文件
create_service_file() {
    local service_type=$1
    local service_name="frp${service_type}"
    local exec_file="/usr/local/frp/frp${service_type}"
    local config_file="/usr/local/frp/frp${service_type}.ini"
    
    cat > "/etc/systemd/system/${service_name}.service" << EOF
[Unit]
Description=FRP ${service_type}
After=network.target

[Service]
Type=simple
ExecStart=${exec_file} -c ${config_file}
Restart=always
RestartSec=5
User=root

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable "${service_name}.service"
    systemctl start "${service_name}.service"
}

# 安装FRP
install_frp() {
    local type=$1
    local version=$(get_latest_version)
    local arch=$(get_arch)
    local filename="frp_${version#v}_linux_${arch}"
    local download_url="https://github.com/fatedier/frp/releases/download/${version}/${filename}.tar.gz"
    
    echo -e "${GREEN}开始安装 FRP ${type}...${NC}"
    echo -e "版本: ${version}"
    echo -e "架构: ${arch}"
    
    # 下载并解压
    echo -e "${YELLOW}下载FRP...${NC}"
    wget -q "$download_url" -O "/tmp/${filename}.tar.gz"
    
    # 备份旧文件
    backup_old_files
    
    # 创建目录并解压
    mkdir -p /usr/local/frp
    tar -xzf "/tmp/${filename}.tar.gz" -C /tmp
    
    # 复制所需文件
    if [ "$type" = "s" ]; then
        cp "/tmp/${filename}/frps" /usr/local/frp/
        cp "/tmp/${filename}/frps.ini" /usr/local/frp/
        create_service_file "s"
    else
        cp "/tmp/${filename}/frpc" /usr/local/frp/
        cp "/tmp/${filename}/frpc.ini" /usr/local/frp/
        create_service_file "c"
    fi
    
    # 清理临时文件
    rm -rf "/tmp/${filename}" "/tmp/${filename}.tar.gz"
    
    echo -e "${GREEN}安装完成!${NC}"
    echo -e "${YELLOW}配置文件位置: /usr/local/frp/frp${type}.ini${NC}"
    echo -e "${YELLOW}请修改配置文件后重启服务：systemctl restart frp${type}${NC}"
}

# 主函数
main() {
    check_root
    check_dependencies
    
    echo -e "${GREEN}FRP 自动安装脚本${NC}"
    echo -e "${YELLOW}请选择安装类型:${NC}"
    echo "1) FRP服务端 (frps)"
    echo "2) FRP客户端 (frpc)"
    read -p "请输入选择 [1/2]: " choice
    
    case "$choice" in
        1)
            install_frp "s"
            ;;
        2)
            install_frp "c"
            ;;
        *)
            echo -e "${RED}无效的选择${NC}"
            exit 1
            ;;
    esac
}

# 运行主函数
main
```