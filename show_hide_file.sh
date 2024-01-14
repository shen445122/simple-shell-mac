#!/bin/sh

if [ $# == 0 ];then
  echo "Input parameter [true or false]"
elif [ "$1" == "true" ];then
  defaults write com.apple.finder AppleShowAllFiles -boolean true ; killall Finder
else
  defaults write com.apple.finder AppleShowAllFiles -boolean false ; killall Finder
fi
