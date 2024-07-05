#########################################################################
# File Name: show_hide_file.sh
# Created Time: Sun Oct 11 17:27:47 2020
# Function: use: 显示mac的隐藏文件
#########################################################################
#!/bin/bash

if [ $# == 0 ];then
  echo "Input parameter [true or false]"
elif [ "$1" == "true" ];then
  defaults write com.apple.finder AppleShowAllFiles -boolean true ; killall Finder
else
  defaults write com.apple.finder AppleShowAllFiles -boolean false ; killall Finder
fi
