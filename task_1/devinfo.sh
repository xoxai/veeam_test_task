#!/bin/bash

# get dev name and path
read -r dev_path < input.txt
dev_name=${dev_path##/dev/}

# using lsblk to get some info
dev_info=`lsblk | grep -i $dev_name`
full_size=`echo $dev_info | awk {'print $4'}`
dev_type=`echo $dev_info | awk {'print $6'}`

# using df to get another info
df_dev_info=`df -hT | grep -i "$dev_path "`
fstype=`echo $df_dev_info | awk {'print $2'}`
free_size=`echo $df_dev_info | awk {'print $5'}`
mount_point=`echo $df_dev_info | awk {'print $7'}`

# print formatted info about device
echo $dev_path $dev_type $full_size $free_size $fstype $mount_point