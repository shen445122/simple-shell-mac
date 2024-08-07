#########################################################################
# File Name: convert_srts.sh
# Created Time: Sun Oct 11 17:27:47 2020
# Function: use: 从字幕文件提取指定的单词
#########################################################################
#!/bin/bash

ls *.srt > list

while read line
do 
    content=`cat "$line" | grep "^[a-zA-Z]"`
    content_deal1=`echo "$content" | sed 's/,//g'` 
    content_deal2=`echo "$content_deal1" | sed 's/\.//g'` 
    for word in ${content_deal2}
    do 
        echo $word >> wordlist.tmp
    done
    > ${line}.words
    cat wordlist.tmp | sort -nr | uniq -c | sort -n > ${line}.words
    /usr/local/bin/dos2unix "${line}.words"
    rm wordlist.tmp

done < list
