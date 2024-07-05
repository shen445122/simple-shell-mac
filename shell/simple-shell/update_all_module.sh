#########################################################################
# File Name: update_all_module.sh
# Created Time: Sun Oct 11 17:27:47 2020
# Function: use: python更新本地模块
#########################################################################
#!/bin/bash

pip freeze --local | grep -v '^-e' | cut -d = -f 1 | xargs -n1 pip install -U -i http://pypi.douban.com/simple/  --trusted-host pypi.douban.com
