#!/bin/sh

if [ $# == 0 ];then
  echo "Input parameter [true or false]"
elif [ "$1" == "true" ];then
  sudo killall -HUP mDNSResponder
else
  echo "[Nothing!!!]"
fi
