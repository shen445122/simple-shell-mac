#!/bin/bash
#########################################################################
# File Name: mysql-install.sh
# Description: macOS/MySQL 安装脚本
# Usage: ./mysql-install.sh [install|start|stop|status|uninstall]
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

# 检查Homebrew
check_brew() {
    if ! command -v brew >/dev/null 2>&1; then
        log_info "安装 Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
}

# 安装MySQL
install_mysql() {
    check_brew
    
    log_info "更新 Homebrew..."
    brew update
    
    log_info "安装 MySQL..."
    brew install mysql
    
    log_info "初始化 MySQL..."
    unset TMPDIR
    mkdir -p /usr/local/var/mysql
    mysql_install_db --verbose --user="$(whoami)" --basedir="$(brew --prefix mysql)" --datadir=/usr/local/var/mysql --tmpdir=/tmp 2>/dev/null || true
    
    log_info "安装完成！"
    log_info "启动命令: mysql.server start"
}

# 启动MySQL
start_mysql() {
    log_info "启动 MySQL..."
    if command -v mysql.server >/dev/null 2>&1; then
        mysql.server start
    elif command -v mysqld >/dev/null 2>&1; then
        mysqld &
    else
        brew services start mysql
    fi
    log_info "MySQL 已启动"
}

# 停止MySQL
stop_mysql() {
    log_info "停止 MySQL..."
    if command -v mysql.server >/dev/null 2>&1; then
        mysql.server stop
    elif command -v mysqld >/dev/null 2>&1; then
        pkill mysqld
    else
        brew services stop mysql
    fi
    log_info "MySQL 已停止"
}

# MySQL状态
status_mysql() {
    if pgrep -x mysqld >/dev/null 2>&1; then
        log_info "MySQL 状态: 运行中"
    else
        log_info "MySQL 状态: 未运行"
    fi
}

# 卸载MySQL
uninstall_mysql() {
    log_warn "卸载 MySQL..."
    brew uninstall mysql
    log_info "卸载完成（数据目录 /usr/local/var/mysql 未删除）"
}

# 重置密码
reset_password() {
    log_info "重置 MySQL root 密码..."
    mysql -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';"
    log_info "密码已重置为: new_password"
}

# 主函数
main() {
    check_macos
    
    local action="${1:-status}"
    
    case "$action" in
        install)
            install_mysql
            ;;
        start)
            start_mysql
            ;;
        stop)
            stop_mysql
            ;;
        restart)
            stop_mysql
            sleep 1
            start_mysql
            ;;
        status)
            status_mysql
            ;;
        uninstall)
            uninstall_mysql
            ;;
        reset)
            reset_password
            ;;
        *)
            echo "用法: $0 [install|start|stop|restart|status|uninstall|reset]"
            echo "  install   - 安装 MySQL"
            echo "  start    - 启动 MySQL"
            echo "  stop     - 停止 MySQL"
            echo "  restart  - 重启 MySQL"
            echo "  status   - 查看状态"
            echo "  uninstall - 卸载 MySQL"
            echo "  reset    - 重置密码"
            ;;
    esac
}

main "$@"
