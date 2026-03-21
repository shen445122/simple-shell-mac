#!/bin/bash
#########################################################################
# File Name: convert_srts.sh
# Description: 从SRT字幕文件提取单词并统计词频
# Usage: ./convert_srts.sh [srt_file.srt]
# Author: shen445122
#########################################################################

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 用法
usage() {
    echo "用法: $0 <srt文件> [输出文件]"
    echo "示例: $0 movie.srt wordlist.txt"
    exit 1
}

# 检查依赖
check_deps() {
    command -v dos2unix >/dev/null 2>&1 || {
        log_info "安装 dos2unix..."
        brew install dos2unix 2>/dev/null || sudo apt-get install -y dos2unix 2>/dev/null || true
    }
}

# 提取单词
extract_words() {
    local srt_file="$1"
    local output="${2:-${srt_file%.srt}.words}"
    
    if [ ! -f "$srt_file" ]; then
        log_error "文件不存在: $srt_file"
        exit 1
    fi
    
    log_info "处理文件: $srt_file"
    log_info "输出文件: $output"
    
    # 提取纯英文行，移除数字和标点，统计词频
    grep -oE '\b[a-zA-Z]+\b' "$srt_file" | \
        tr '[:upper:]' '[:lower:]' | \
        sort | \
        uniq -c | \
        sort -rn > "$output"
    
    # 转换格式（如果dos2unix可用）
    if command -v dos2unix >/dev/null 2>&1; then
        dos2unix "$output" 2>/dev/null || true
    fi
    
    local word_count=$(wc -l < "$output")
    log_info "完成！提取了 $word_count 个唯一单词"
    log_info "结果保存在: $output"
}

# 主函数
main() {
    check_deps
    
    if [ $# -eq 0 ]; then
        usage
    fi
    
    extract_words "$@"
}

main "$@"
