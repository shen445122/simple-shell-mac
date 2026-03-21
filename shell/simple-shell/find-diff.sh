#!/bin/bash
#########################################################################
# File Name: find-diff.sh
# Description: 比较两个目录，找出新增文件
# Usage: ./find-diff.sh <旧目录> <新目录> [输出目录]
# Author: shen445122
#########################################################################

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 用法
usage() {
    echo "用法: $0 <旧目录> <新目录> [输出目录]"
    echo ""
    echo "示例:"
    echo "  $0 /path/old /path/new          # 比较并输出到 default_diff_dir"
    echo "  $0 /path/old /path/new ./diff   # 输出到 ./diff 目录"
    exit 1
}

# 主函数
main() {
    local old_dir="$1"
    local new_dir="$2"
    local diff_dir="${3:-default_diff_dir}"
    
    # 检查参数
    if [ -z "$old_dir" ] || [ -z "$new_dir" ]; then
        usage
    fi
    
    # 检查目录
    if [ ! -d "$old_dir" ]; then
        log_error "旧目录不存在: $old_dir"
        exit 1
    fi
    
    if [ ! -d "$new_dir" ]; then
        log_error "新目录不存在: $new_dir"
        exit 1
    fi
    
    log_info "旧目录: $old_dir"
    log_info "新目录: $new_dir"
    log_info "输出目录: $diff_dir"
    
    # 创建输出目录
    mkdir -p "$diff_dir"
    
    # 获取文件列表
    log_info "扫描文件..."
    find "$new_dir" -type f -printf "%f\n" | sort > "${diff_dir}/new_files.txt"
    find "$old_dir" -type f -printf "%f\n" | sort > "${diff_dir}/old_files.txt"
    
    local old_count=$(wc -l < "${diff_dir}/old_files.txt")
    local new_count=$(wc -l < "${diff_dir}/new_files.txt")
    
    log_info "旧目录文件数: $old_count"
    log_info "新目录文件数: $new_count"
    
    # 找出新增文件
    log_info "对比差异..."
    comm -13 "${diff_dir}/old_files.txt" "${diff_dir}/new_files.txt" > "${diff_dir}/diff_files.txt"
    
    local diff_count=$(wc -l < "${diff_dir}/diff_files.txt")
    log_info "新增文件数: $diff_count"
    
    # 复制新增文件
    if [ "$diff_count" -gt 0 ]; then
        log_info "复制新增文件到输出目录..."
        while read -r filename; do
            local source_file=$(find "$new_dir" -type f -name "$filename" | head -1)
            if [ -n "$source_file" ]; then
                cp -v "$source_file" "$diff_dir/"
            fi
        done < "${diff_dir}/diff_files.txt"
        log_info "完成！新增文件已复制到: $diff_dir"
    else
        log_warn "没有发现新增文件"
    fi
    
    # 清理临时文件
    rm -f "${diff_dir}/old_files.txt" "${diff_dir}/new_files.txt"
    
    log_info "对比完成！"
}

main "$@"
