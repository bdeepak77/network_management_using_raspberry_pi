#!/bin/bash
#############################################
#Author: Vikash and Deepak
#Description: This file takes backup of database
#             every one month
#############################################
date=$(date +%F)
#command to take backup of database
mysqldump -u root -pcs5113@123 ne > $date-ne.sql
#delete everything from database table "device_data"
mysql -h localhost -uroot -pcs5113@123 ne -e "delete from device_data" 
