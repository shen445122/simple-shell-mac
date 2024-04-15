#!/bin/sh

tmpfile="tmp.dat"
infofile="dragonhead.dat"
notfile="notfound.list"
allfile="tableall"

echo '' > ${tmpfile}
while read Line
do
  name=`echo $Line | awk '{print $1}'`
  grep $name ${allfile}
  if [ $? == 0 ];then
    grep $name ${allfile} | awk '{print $2,$1}'>> ${tmpfile}
  else
    echo $Line >> ${notfile}
  fi
done < ${infofile}
