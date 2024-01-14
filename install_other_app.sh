#!/bin/sh

if [ $# == 0 ];then
  echo "Input parameter [APP NAME in /Applications]"
else
  APP=$1
  sudo spctl --master-disable
  sudo xattr -d com.apple.quarantine /Applications/"$APP"
fi
