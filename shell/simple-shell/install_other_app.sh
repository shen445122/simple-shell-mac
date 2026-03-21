#!/bin/bash
#########################################################################
# File Name: install_other_app.sh
# Description: 允许运行第三方应用 (关闭Gatekeeper)
# Usage: ./install_other_app.sh [app_name|status|enable|disable]
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

# 检查是否为macOS
check_macos() {
    if [[ "$OSTYPE" != "darwin"* ]]; then
        log_error "此脚本仅适用于 macOS"
        exit 1
    fi
}

# 检查root权限
check_root() {
    if [ "$EUID" -ne 0 ]; then
        log_error "请使用 sudo 运行此脚本"
        exit 1
    fi
}

# 获取Gatekeeper状态
status_gatekeeper() {
    local status=$(spctl --status 2>/dev/null | awk '{print $2}')
    case "$status" in
        disabled)
            log_info "Gatekeeper状态: 已关闭 (允许所有来源)"
            ;;
        enabled)
            log_info "Gatekeeper状态: 已开启"
            # 显示当前允许的来源
            spctl --status --verbose 2>/dev/null | grep -E "^[0-9]" || true
            ;;
        *)
            log_warn "Gatekeeper状态未知: $status"
            ;;
    esac
}

# 允许第三方应用
enable_third_party() {
    log_info "关闭 Gatekeeper..."
    spctl --master-disable
    log_info "完成！已允许所有来源的应用"
    log_warn "安全提示: 建议仅在必要时关闭，使用后及时恢复"
}

# 禁用第三方应用
disable_third_party() {
    log_info "开启 Gatekeeper..."
    spctl --master-enable
    log_info "完成！已恢复默认安全设置"
}

# 移除应用隔离属性
remove_quarantine() {
    local app_name="$1"
    
    if [ -z "$app_name" ]; then
        log_error "请指定应用名称"
        echo "用法: $0 <应用名称> [应用路径]"
        echo "示例: $0 Xcode /Applications/Xcode.app"
        exit 1
    fi
    
    # 处理路径
    local app_path="$app_name"
    if [[ ! "$app_path" == *".app"* ]]; then
        app_path="/Applications/${app_name}.app"
    fi
    
    if [ ! -d "$app_path" ]; then
        log_error "应用不存在: $app_path"
        exit 1
    fi
    
    log_info "移除隔离属性: $app_path"
    xattr -d com.apple.quarantine "$app_path" 2>/dev/null || true
    log_info "完成！"
}

# 主函数
main() {
    check_macos
    
    local action="${1:-status}"
    
    case "$action" in
        status)
            status_gatekeeper
            ;;
        enable)
            check_root
            enable_third_party
            ;;
        disable)
            check_root
            disable_third_party
            ;;
        *)
            # 尝试作为应用名称处理
            remove_quarantine "$action"
            ;;
    esac
}

main "$@"
