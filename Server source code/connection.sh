#!/bin/bash
########################################################################################################
# Author: Vikash and Deepak
# Place: Server
# Description: Main job of this script is to loop through all the files send by raspberrypi and for each file 
#			   call 'connection.py' which will parse each file and enter the data into the database. Raspberrypi
#			   is configured to send all the files to '/home/cs5113/networks/files/' folder.
# Requirements: Python 2.6+
#	Copyright (c) 2014 Vikash And Deepak
# 	This script is licensed under GNU GPL version 2.0 or above
###########################################################################################################

FILES=/home/cs5113/networks/files/*
DIR="/home/cs5113/networks/files"
while :
do 
	for f in $FILES
	do
		#check if the dir is empty or not
		if [ "$(ls -A $DIR)" ] ; then
		sudo chmod 777 $f
			# for each file call connection.py to enter data present
			# in the file to database
			python connection.py $f
			
		fi
	done
	
done
