#!/bin/sh

# 定义颜色代码（若终端不支持颜色则自动忽略）
if [ -t 1 ]; then
  RED='\033[1;31m'
  GREEN='\033[1;32m'
  YELLOW='\033[1;33m'
  BLUE='\033[1;34m'
  CYAN='\033[1;36m'
  RESET='\033[0m'
else
  RED='' GREEN='' YELLOW='' BLUE='' CYAN='' RESET=''
fi

# 检测系统架构
get_arch() {
  if command -v arch >/dev/null 2>&1; then
    platform=$(arch)
  else
    platform=$(uname -m)
  fi

  case "$platform" in
    x86_64)    ARCH="amd64" ;;
    aarch64)   ARCH="arm64" ;;
    armv7l)    ARCH="armv7" ;;
    i386)      ARCH="i386" ;;
    *)         ARCH="${RED}Unsupported ($platform)${RESET}" ;;
  esac
  echo "$ARCH"
}

# 检测操作系统类型
get_os() {
  case "$(uname)" in
    Linux)     OS="Linux" ;;
    Darwin)    OS="macOS" ;;
    FreeBSD)   OS="FreeBSD" ;;
    OpenBSD)   OS="OpenBSD" ;;
    NetBSD)    OS="NetBSD" ;;
    CYGWIN*|MINGW*|MSYS*) OS="Windows" ;;
    *)         OS="Unknown" ;;
  esac
  echo "$OS"
}

# 获取发行版信息
get_distro() {
  if command -v lsb_release >/dev/null 2>&1; then
    DISTRO_ID=$(lsb_release -si)
    DISTRO_DESC=$(lsb_release -sd | tr -d '"')
    DISTRO_RELEASE=$(lsb_release -sr)
    DISTRO_CODENAME=$(lsb_release -sc)
  elif [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO_ID=$ID
    DISTRO_DESC=$PRETTY_NAME
    DISTRO_RELEASE=$VERSION_ID
    DISTRO_CODENAME=$VERSION_CODENAME
  elif command -v sw_vers >/dev/null 2>&1; then
    DISTRO_ID="macOS"
    DISTRO_DESC=$(sw_vers -productName)
    DISTRO_RELEASE=$(sw_vers -productVersion)
    DISTRO_CODENAME="-"
  elif [ "$(uname)" = "FreeBSD" ]; then
    DISTRO_ID="FreeBSD"
    DISTRO_DESC=$(freebsd-version)
    DISTRO_RELEASE=$(freebsd-version | cut -d'-' -f1)
    DISTRO_CODENAME="-"
  else
    DISTRO_ID="Unknown"
    DISTRO_DESC="Not Detected"
    DISTRO_RELEASE="-"
    DISTRO_CODENAME="-"
  fi
  echo "$DISTRO_ID|$DISTRO_DESC|$DISTRO_RELEASE|$DISTRO_CODENAME"
}

# 获取信息
ARCH=$(get_arch)
OS=$(get_os)
KERNEL=$(uname -r)
DISTRO_INFO=$(get_distro)
DISTRO_ID=$(echo "$DISTRO_INFO" | cut -d'|' -f1)
DISTRO_DESC=$(echo "$DISTRO_INFO" | cut -d'|' -f2)
DISTRO_RELEASE=$(echo "$DISTRO_INFO" | cut -d'|' -f3)
DISTRO_CODENAME=$(echo "$DISTRO_INFO" | cut -d'|' -f4)

# 输出格式化信息
echo -e "${CYAN}╒════════════════════════════════════════════╕${RESET}"
echo -e "${CYAN}│          ${GREEN}SYSTEM INFORMATION REPORT${CYAN}          │${RESET}"
echo -e "${CYAN}╞════════════════════════════════════════════╡${RESET}"
printf "${BLUE}%-16s${RESET} : ${YELLOW}%s${RESET}\n" "OS Platform"   "$OS"
printf "${BLUE}%-16s${RESET} : ${YELLOW}%s${RESET}\n" "Distribution" "$DISTRO_DESC"
printf "${BLUE}%-16s${RESET} : ${YELLOW}%s${RESET}\n" "Release"      "$DISTRO_RELEASE"
printf "${BLUE}%-16s${RESET} : ${YELLOW}%s${RESET}\n" "Codename"     "$DISTRO_CODENAME"
printf "${BLUE}%-16s${RESET} : ${YELLOW}%s${RESET}\n" "Kernel"       "$KERNEL"
printf "${BLUE}%-16s${RESET} : ${YELLOW}%s${RESET}\n" "Architecture" "$ARCH"
echo -e "${CYAN}╘════════════════════════════════════════════╛${RESET}"

# 架构不支持警告
if [[ $ARCH == *"Unsupported"* ]]; then
  echo -e "\n${RED}⚠ WARNING: Unsupported architecture detected.${RESET}"
  echo -e "${YELLOW}Some tools may not function properly.${RESET}"
fi