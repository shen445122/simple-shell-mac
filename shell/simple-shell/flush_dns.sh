#!/bin/bash
#########################################################################
# File Name: flush_dns.sh
# Description: 刷新DNS缓存
# Usage: ./flush_dns.sh [macos|all]
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

# 检测操作系统
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    else
        echo "unknown"
    fi
}

# macOS DNS刷新
flush_dns_macos() {
    local version=$(sw_vers -productVersion | cut -d. -f1)
    
    log_info "刷新 macOS DNS缓存..."
    
    if [ "$version" -ge 12 ]; then
        # Monterey 及更新版本
        sudo dscacheutil -flushcache
        sudo killall -HUP mDNSResponder
        log_info "DNS缓存已刷新 (macOS 12+)"
    else
        # 旧版本
        sudo killall -HUP mDNSResponder
        log_info "DNS缓存已刷新 (旧版macOS)"
    fi
}

# Linux DNS刷新
flush_dns_linux() {
    log_info "刷新 Linux DNS缓存..."
    
    # 尝试 systemd-resolved
    if command -v systemd-resolve >/dev/null 2>&1; then
        sudo systemd-resolve --flush-caches
        log_info "systemd-resolved 缓存已刷新"
    elif command -v resolvectl >/dev/null 2>&1; then
        sudo resolvectl flush-caches
        log_info "resolvectl 缓存已刷新"
    elif command -v service >/dev/null 2>&1; then
        sudo service nscd restart 2>/dev/null || log_warn "nscd 服务不可用"
        log_info "nscd 服务已重启"
    else
        log_error "无法刷新: 未找到合适的DNS服务"
        exit 1
    fi
}

# 显示状态
show_status() {
    local os=$(detect_os)
    log_info "当前系统: $os"
    
    case "$os" in
        macos)
            log_info "DNS缓存状态: macOS 使用 mDNSResponder"
            ;;
        linux)
            if command -v systemd-resolve >/dev/null 2>&1; then
                systemd-resolve --statistics 2>/dev/null | grep -i "cache" || true
            fi
            ;;
    esac
}

# 主函数
main() {
    local mode="${1:-macos}"
    local os=$(detect_os)
    
    case "$mode" in
        macos)
            if [ "$os" != "macos" ]; then
                log_error "当前系统不是 macOS"
                exit 1
            fi
            flush_dns_macos
            ;;
        linux)
            if [ "$os" != "linux" ]; then
                log_error "当前系统不是 Linux"
                exit 1
            fi
            flush_dns_linux
            ;;
        all)
            flush_dns_macos 2>/dev/null || true
            flush_dns_linux 2>/dev/null || true
            ;;
        status)
            show_status
            ;;
        *)
            echo "用法: $0 [macos|linux|all|status]"
            echo "  macos  - 刷新 macOS DNS (默认)"
            echo "  linux  - 刷新 Linux DNS"
            echo "  all    - 刷新所有系统DNS"
            echo "  status - 显示DNS状态"
            ;;
    esac
}

main "$@"
