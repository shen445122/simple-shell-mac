#!/bin/bash
#########################################################################
# File Name: update_all_module.sh
# Description: 更新Python本地模块
# Usage: ./update_all_module.sh [pip|pip3|conda] [--dry-run]
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

# 检测Python
detect_python() {
    if command -v python3 >/dev/null 2>&1; then
        echo "python3"
    elif command -v python >/dev/null 2>&1; then
        echo "python"
    else
        log_error "未找到 Python"
        exit 1
    fi
}

# 检测pip
detect_pip() {
    if command -v pip3 >/dev/null 2>&1; then
        echo "pip3"
    elif command -v pip >/dev/null 2>&1; then
        echo "pip"
    else
        log_error "未找到 pip"
        exit 1
    fi
}

# 获取当前pip版本
get_pip_version() {
    $PIP --version | awk '{print $2}'
}

# 更新模块
update_modules() {
    local dry_run="$1"
    local pip_version=$(get_pip_version)
    
    log_info "Python: $($PYTHON --version)"
    log_info "pip: $pip_version"
    log_info "开始检查可更新模块..."
    
    if [ "$dry_run" = "true" ]; then
        log_info "[Dry Run] 以下模块可更新:"
        $PIP list -o | grep -v "^-e" | head -20
        log_info "[Dry Run] 实际更新已跳过"
    else
        log_info "更新所有本地模块..."
        
        # 排除 editable 安装的包
        $PIP freeze --local | grep -v '^-e' | cut -d '=' -f 1 | while read -r package; do
            log_info "更新: $package"
            $PIP install -U "$package" --quiet 2>/dev/null || log_warn "更新失败: $package"
        done
        
        log_info "更新完成！"
    fi
}

# 清理缓存
clean_cache() {
    log_info "清理 pip 缓存..."
    $PIP cache purge 2>/dev/null || true
    log_info "缓存已清理"
}

# 显示过期包
list_outdated() {
    log_info "过期包列表:"
    $PIP list -o
}

# 主函数
main() {
    local PYTHON=$(detect_python)
    local PIP=$(detect_pip)
    local dry_run="false"
    
    # 解析参数
    for arg in "$@"; do
        case "$arg" in
            --dry-run)
                dry_run="true"
                ;;
            --clean)
                clean_cache
                exit 0
                ;;
            --list|-l)
                list_outdated
                exit 0
                ;;
        esac
    done
    
    update_modules "$dry_run"
}

main "$@"
