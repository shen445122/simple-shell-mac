#!/bin/bash
#########################################################################
# File Name: show_hide_file.sh
# Description: 显示/隐藏 macOS 隐藏文件
# Usage: ./show_hide_file.sh [show|hide|toggle|status]
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

# 检查macOS
check_macos() {
    if [[ "$OSTYPE" != "darwin"* ]]; then
        log_error "此脚本仅适用于 macOS"
        exit 1
    fi
}

# 获取当前状态
show_status() {
    local status=$(defaults read com.apple.finder AppleShowAllFiles 2>/dev/null)
    if [ "$status" = "1" ]; then
        log_info "隐藏文件: 显示"
    else
        log_info "隐藏文件: 隐藏"
    fi
}

# 显示隐藏文件
show_files() {
    log_info "显示隐藏文件..."
    defaults write com.apple.finder AppleShowAllFiles -bool true
    killall Finder
    log_info "完成！Finder 已重启"
}

# 隐藏隐藏文件
hide_files() {
    log_info "隐藏隐藏文件..."
    defaults write com.apple.finder AppleShowAllFiles -bool false
    killall Finder
    log_info "完成！Finder 已重启"
}

# 切换状态
toggle_files() {
    local status=$(defaults read com.apple.finder AppleShowAllFiles 2>/dev/null)
    if [ "$status" = "1" ]; then
        hide_files
    else
        show_files
    fi
}

# 主函数
main() {
    check_macos
    
    local action="${1:-status}"
    
    case "$action" in
        show|true|1)
            show_files
            ;;
        hide|false|0)
            hide_files
            ;;
        toggle)
            toggle_files
            ;;
        status)
            show_status
            ;;
        *)
            echo "用法: $0 [show|hide|toggle|status]"
            echo "  show   - 显示隐藏文件"
            echo "  hide   - 隐藏隐藏文件"
            echo "  toggle - 切换显示/隐藏"
            echo "  status - 查看当前状态"
            ;;
    esac
}

main "$@"
