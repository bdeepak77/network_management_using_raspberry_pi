#!/bin/bash
########################################################################################################
# Author: Vikash and Deepak
# Place: Raspberry Pi
# Description: This file generates a output file which is placed in 'files_to_send' dir
#              which is then send to the server by another script 'files_ssh.sh'. 
#              File can be made to run after specific interval.
#			   "iwlist scan" gives details about every AP which is broadcasting its presence in the vicinity
#              For more info on "iwlist scan " please do 'man iwlist' or google it.
# Contains of the generated file: device_id of raspberrypi
#								  Ipv4 addresses of raspberrypi extracted by 'regex expression' from 'ifconfig'
#								  Token -> to tell the server which is the latest file send by raspberryppi
#								  Output of 'iwlist scan' command in a nice tabular fromat done by 'iwlist.py' file
#
#	Copyright (c) 2014 Vikash And Deepak
# 	This script is licensed under GNU GPL version 2.0 or above
###########################################################################################################
c=0
a=0
device_id=0
while [ $c -lt 1 ];
do
	#device_id into the file
	echo "$device_id" > files_to_send/f$device_idile$a.txt
	#getting the ip addr and writing to file
	#change 'ra0' to 'wlan0' if you r using different wifi dongle other then GW-450D
	ifconfig ra0 | sed -n 's/.*inet *addr:\([0-9\.]*\).*/\1/p' >> files_to_send/f$device_idile$a.txt
	#token to allow server to find out the latest file send by raspberry pi
	echo "token=$a" >> files_to_send/f$device_idile$a.txt
	#Generating the output of iwlist and parsing it via iwlist.py and then writing it to output file
	#change 'ra0' to 'wlan0' if you r using different wifi dongle other then GW-450D
	iwlist ra0 scan | python iwlist.py >> files_to_send/f$device_idile$a.txt
	((a++))
	#Change it if you want to generated the output at a different interval
	sleep 30s
done
