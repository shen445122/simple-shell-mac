#!/bin/bash
#########################################################################
# File Name: disk_no_limit_speed.sh
# Description: 加快 Time Machine 备份速度（禁用节流）
# Usage: sudo ./disk_no_limit_speed.sh [on|off|status]
# Author: shen445122
#########################################################################

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 检查是否为root
check_root() {
    if [ "$EUID" -ne 0 ]; then
        log_error "请使用 sudo 运行此脚本"
        exit 1
    fi
}

# 状态查询
show_status() {
    local status=$(sysctl debug.lowpri_throttle_enabled 2>/dev/null | awk '{print $2}')
    if [ "$status" = "0" ]; then
        log_info "当前状态: 已启用高速模式 (lowpri_throttle_enabled=0)"
    else
        log_info "当前状态: 默认节流模式 (lowpri_throttle_enabled=1)"
    fi
}

# 启用高速模式
enable_fast() {
    log_info "启用高速备份模式..."
    sysctl debug.lowpri_throttle_enabled=0
    log_info "完成！Time Machine 备份速度应该会明显提升"
    log_warn "注意: 此设置重启后失效，如需永久生效可添加到启动脚本"
}

# 禁用高速模式
disable_fast() {
    log_info "恢复默认节流模式..."
    sysctl debug.lowpri_throttle_enabled=1
    log_info "完成！"
}

# 主函数
main() {
    check_root
    
    case "${1:-status}" in
        on)
            enable_fast
            ;;
        off)
            disable_fast
            ;;
        status|*)
            show_status
            ;;
    esac
}

main "$@"
