#########################################################################
# File Name: mysql-install.sh
# Created Time: Sun Oct 11 17:27:47 2020
# Function: use: mac安装mysql
#########################################################################
#!/bin/bash

brew update # 这是一个好习惯
brew install mysql
# 使用 MySQL 前，我们需要做一些设置：
unset TMPDIR
mkdir /usr/local/var
mysql_install_db --verbose --user=`whoami` --basedir="$(brew --prefix mysql)" --datadir=/usr/local/var/mysql --tmpdir=/tmp