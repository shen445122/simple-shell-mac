#########################################################################
# File Name: flush_dns.sh
# Created Time: Sun Oct 11 17:27:47 2020
# Function: use: 刷新DNS换成
#########################################################################
#!/bin/bash

if [ $# == 0 ];then
  echo "Input parameter [true or false]"
elif [ "$1" == "true" ];then
  sudo killall -HUP mDNSResponder
else
  echo "[Nothing!!!]"
fi
