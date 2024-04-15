#!/bin/sh

count1=0
count2=0
while true
do
  ping -c 1 baidu.com | grep 'bytes from'
  ret=$?
  if [ $ret == 1 ];then
     echo "[ERROR] [$count1] wifi connect lost,restart it..." && sleep 1
     networksetup -setairportpower en0 off && sleep 1
     networksetup -setairportpower en0 on
     count1=$(($count1 + 1))
     sleep 5
  else
     echo "[OK] [$count2] wifi connect is running well!"
     count2=$(($count2 + 1))
  fi
sleep 2
done
