#########################################################################
# File Name: find-diff.sh
# Created Time: Sun Oct 11 17:27:47 2020
# Function: use: sh finddiff.sh olddir newdir
#########################################################################
#!/bin/bash

OLD_FILE_DIR="$1"
NEW_FILE_DIR="$2"
DIFF_FILE_DIR="$3"
LOG_FILE=finddiff_`date +%Y%m%d`.log

getFileList(){
	local_file_dir=$1
    local_file_list=$1.txt

    if [ ! -f $local_file_list ];then
		if [ -d $local_file_dir ];then
			find $local_file_dir -type f > $local_file_list
		else
			echo "dir not find:$local_file_dir"
			exit 1
		fi
	else
		echo "file exit:$local_file_list.please remove it"
		exit 1
    fi

}

wlog(){
    echo "[`date`] $1" | tee -a $LOG_FILE
}

main(){
    wlog "start mission"
    
	if [ "$DIFF_FILE_DIR" == "" ];then
		wlog "no input diff dir,give the diff name to it"
		DIFF_FILE_DIR="default_diff_dif"
	fi
	
    if [ -d $DIFF_FILE_DIR ];then
    	wlog "there are diff dir,do nothing"
    else
    	wlog "there are not diff dir found,make it:$DIFF_FILE_DIR"
    	mkdir $DIFF_FILE_DIR
    fi
    
    wlog "start get old file list form old file dir"
    getFileList $OLD_FILE_DIR
    wlog "get old file list done"
    wlog "start get new file list form new file dir"
    getFileList $NEW_FILE_DIR
    wlog "get new file list done"
    
    OLD_FILE_LIST=$OLD_FILE_DIR.txt
    NEW_FILE_LIST=$NEW_FILE_DIR.txt
    
	COU_OLD_FILE_LIST=`wc -l $OLD_FILE_LIST`
	COU_NEW_FILE_LIST=`wc -l $NEW_FILE_LIST`

	wlog "there are [$COU_OLD_FILE_LIST] files in old dir"
	wlog "there are [$COU_NEW_FILE_LIST] files in new dir"
   	wlog "start get file diff"
    local_count=1

    for new_file in `cat $NEW_FILE_LIST`
    	do 
    		abs_file=`echo ${new_file} | awk -F'/' '{print $NF}'`
			wlog "all files [$COU_NEW_FILE_LIST], deal with file [$local_count] [$abs_file]"
    		grep $abs_file $OLD_FILE_LIST > /dev/null 2>&1
    		if [ "$?" == "0" ];then
                wlog "[$abs_file] in old and new dir,skip it"
    		else
    			wlog "[$abs_file] is new file,copy it into diff dir [$DIFF_FILE_DIR]"
    			mkdir -p $DIFF_FILE_DIR
    			cp $new_file $DIFF_FILE_DIR
    		fi
			local_count=$(( $local_count + 1))
    	done
    
    wlog "scan all new file in new file list done"

	wlog "clear tmp file:$OLD_FILE_LIST,$NEW_FILE_LIST"
	if [ -f $OLD_FILE_LIST ];then
        rm $OLD_FILE_LIST 
		wlog "clear old list file done"
	fi
	if [ -f $NEW_FILE_LIST ];then
		rm $NEW_FILE_LIST
		wlog "clear new list file done"
	fi
}

main
