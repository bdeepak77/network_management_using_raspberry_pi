#!/bin/bash

########################################################################################################
# Author: Vikash and Deepak
# Place: Raspberry Pi
# Description: Main job of this script is that it finds out all the files in 'files_to_send' and then
#			   uses scp and sshpass to send those files to server. It first check whether server is 
#			   reachable or not. If it is then only it does scp and delete the file else it doesn't do
#				anything to the files and tries after sometime.
# Requirements: sshpass,scp,ping
#				apt-get install sshpass
#
#	Copyright (c) 2014 Vikash And Deepak
# 	This script is licensed under GNU GPL version 2.0 or above
###########################################################################################################
FILES=/home/pi/Desktop/files_to_send/*
DIR="/home/pi/Desktop/files_to_send"
#addr of server
server="192.168.7.27"
while :
do 
	for f in $FILES
	do
		# check if the dir is empty or not
		if [ "$(ls -A $DIR)" ] ; then
		#changes the permission of files
		sudo chmod 777 $f
			#ping server to check if it is reachable
			if ping -c1 $server >/dev/null; then
				# sending the file to server
				# if server requires pwd to do scp then use sshpass
				# use google to find more about 'sshpass'
				sshpass -p rpms@123 scp $f cs5113@192.168.7.27:/home/cs5113/networks/files/
				# delete the file already processed
				rm $f
			fi
		echo "done"
		fi
	done
	#sleep for some time
	sleep 30s
done
