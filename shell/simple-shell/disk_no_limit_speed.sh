#########################################################################
# File Name: disk_no_limit_speed.sh
# Created Time: Fri Mar 20 22:36:11 2020
# Function: 加快时间机器的备份速度
#########################################################################
#!/bin/bash

sudo sysctl debug.lowpri_throttle_enabled=0
