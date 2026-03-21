#!/bin/bash
#########################################################################
# File Name: auto_restart_mac_wifi.sh
# Description: 自动检测网络，如果不通则重启WiFi
# Usage: ./auto_restart_mac_wifi.sh [interval]
# Author: shen445122
#########################################################################

INTERVAL=${1:-2}  # 默认检测间隔(秒)
MAX_LOG_LINES=100  # 最大日志行数
LOG_FILE="/tmp/wifi_monitor_$(date +%Y%m%d).log"

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "$msg" | tee -a "$LOG_FILE"
    
    # 限制日志文件大小
    if [ -f "$LOG_FILE" ]; then
        tail -n $MAX_LOG_LINES "$LOG_FILE" > "${LOG_FILE}.tmp" && mv "${LOG_FILE}.tmp" "$LOG_FILE"
    fi
}

# 检测WiFi接口
get_wifi_interface() {
    networksetup -listallhardwareports | grep -A1 "Wi-Fi" | grep "Device" | awk '{print $2}'
}

# 检查网络连接
check_network() {
    ping -c 1 -W 2 baidu.com >/dev/null 2>&1
    return $?
}

# 重启WiFi
restart_wifi() {
    local wifi_dev=$(get_wifi_interface)
    if [ -z "$wifi_dev" ]; then
        log "[ERROR] 无法找到WiFi接口"
        return 1
    fi
    
    log "[INFO] 正在重启WiFi: $wifi_dev"
    networksetup -setairportpower "$wifi_dev" off
    sleep 1
    networksetup -setairportpower "$wifi_dev" on
    sleep 3
    log "[INFO] WiFi已重启"
}

# 主循环
main() {
    local fail_count=0
    local success_count=0
    
    log "[INFO] WiFi监控启动，检测间隔: ${INTERVAL}秒"
    log "[INFO] WiFi接口: $(get_wifi_interface)"
    
    while true; do
        if check_network; then
            success_count=$((success_count + 1))
            log "[OK] 网络正常 (成功: $success_count, 失败: $fail_count)"
        else
            fail_count=$((fail_count + 1))
            log "[ERROR] 网络连接失败 (成功: $success_count, 失败: $fail_count)"
            restart_wifi
        fi
        
        sleep "$INTERVAL"
    done
}

# 优雅退出
trap 'log "[INFO] 收到退出信号，正在停止..."; exit 0' SIGINT SIGTERM

main
