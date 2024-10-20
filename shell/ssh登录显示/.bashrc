# ~/.bashrc: executed by bash(1) for non-login shells.

# Note: PS1 and umask are already set in /etc/profile. You should not
# need this unless you want different defaults for root.
# PS1='${debian_chroot:+($debian_chroot)}\h:\w\$ '
# umask 022

# You may uncomment the following lines if you want `ls' to be colorized:
# export LS_OPTIONS='--color=auto'
# eval "$(dircolors)"
# alias ls='ls $LS_OPTIONS'
# alias ll='ls $LS_OPTIONS -l'
# alias l='ls $LS_OPTIONS -lA'
#
# Some more alias to avoid making mistakes:
# alias rm='rm -i'
# alias cp='cp -i'
# alias mv='mv -i'

# 开启SSH服务
#sshd

# 获取公网IPv6地址
ipv6=$(curl -s -6 ifconfig.co)

# 清屏
clear

# Dedian12欢迎语

echo ""
echo "  █████╗ ██╗   ██╗███████╗██████╗  █████╗ ███╗   ██╗"
echo " ██╔══██╗██║   ██║██╔════╝██╔══██╗██╔══██╗████╗  ██║"
echo " ███████║██║   ██║█████╗  ██████╔╝███████║██╔██╗ ██║"
echo " ██╔══██║╚██╗ ██╔╝██╔══╝  ██╔═══╝ ██╔══██║██║╚██╗██║"
echo " ██║  ██║ ╚████╔╝ ███████╗██║     ██║  ██║██║ ╚████║"
echo " ╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝"
echo ""
echo " ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "                         欢迎使用 Debian 12"
echo " ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo " 这里是您的个人工作区，愿您每一次敲击都是对知识的探索和创造。"
echo ""
echo " 您的公网IPv6地址是：$ipv6"
echo ""

# 定时任务
export EDITOR=vim

# cloudflare解析（后台运行）  
#bash /data/data/com.termux/files/home/ipv6-notify/cloudflare_ipv6.sh >/dev/null 2>&1 &  

# ipv6通知
#bash /data/data/com.termux/files/home/ipv6_notify/ipv6_notify.sh >/dev/null 2>&1 &

# 网络文件管理
#bash ~/.filebrowser/filebrowser -a 0.0.0.0 -p 8001 -r /data/data/com.termux/files >/dev/null 2>&1 &