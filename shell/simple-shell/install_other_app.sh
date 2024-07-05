#########################################################################
# File Name: install_other_app.sh
# Created Time: Sun Oct 11 17:27:47 2020
# Function: use: mac安装并支持第三方app开启
#########################################################################
#!/bin/bash

if [ $# == 0 ];then
  echo "Input parameter [APP NAME in /Applications]"
else
  APP=$1
  sudo spctl --master-disable
  sudo xattr -d com.apple.quarantine /Applications/"$APP"
fi
