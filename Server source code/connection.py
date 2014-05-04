
#!/usr/bin/python
########################################################################################################
# Author: Vikash and Deepak
# Place: Raspberry Pi
# Description: This python file will parse the files send by raspberrypi and put it accordingly in database
# Requirements : mysql.connector
#				downlaod link: http://dev.mysql.com/downloads/connector/python/
#				installation: dpkg -i file_name.deb
#	Copyright (c) 2014 Vikash And Deepak
# 	This script is licensed under GNU GPL version 2.0 or above
###########################################################################################################
import mysql.connector
from mysql.connector import errorcode
import threading
import os
import subprocess
import time
from math import radians, cos, sin, asin,sqrt,atan2,log10
import sys

#configuration to connnet to mysql database
config = {
  'user': 'root',
  'password': 'cs5113@123',
  'host': '127.0.0.1',
  'database': 'ne',
  'raise_on_warnings': True,
}
#error handlling if python is not able to connect to database
try:
  cnx = mysql.connector.connect(**config)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exists")
  else:
    print(err)
# setting the cursor
cursor = cnx.cursor()
print "done till here"

#function to find out the distance between between pair of latitude and longitude
def distance(lat11,lat22,lon11,lon22):
    R = 6373.0

    lat1 = radians(lat11)
    lon1 = radians(lon11)
    lat2 = radians(lat22)
    lon2 = radians(lon22)

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    return distance


#get the input file via command line argument
file = open(sys.argv[1])
i=0
pi_id=0
token=0
while 1:
    i=i+1
    line = file.readline()
    if not line:
        break
    a=line.split()
    if(i==1):
      pi_id= int(a[0]) # find the raspberry pi id
      
    if(i==2):
      ip=a[0] #get the ip addr of raspberrypi
      cursor.execute("select count(device_id) from device_info where device_id= %d "%(pi_id))
      count1=cursor.fetchone()
      cnx.commit()
      if(count1[0]==1):
		#update the ip addr. of raspberry pi
        readsql= "update device_info set ip = '%s' where device_id = %d"%((ip),(pi_id))
        cursor.execute(readsql)
        cnx.commit      
    if(i==3):
      token= int(a[0].split('=')[-1]) #extract the token number
      print token
    if(a[0]=="IITH" or a[0]=="IITH-1" or a[0]=="IITH-Guest" or a[0]=="Test1"):
	  #check if Acess point is already present in device_info or not
      cursor.execute("select count(mac) from device_info where mac like %s and latitude!=0 and longitude!=0",[a[1]])
      count = cursor.fetchone()
      cnx.commit()
      print count
      if(count[0]==1):
        print "in"
		#get the device_id corresponding to mac read from file
        cursor.execute("select device_id,latitude,longitude from device_info where mac like %s",[a[1]])
        device = cursor.fetchone()
        cnx.commit()
		#get latitude and logitude from device_info
        cursor.execute("select latitude,longitude from device_info where device_id like %s",[pi_id])
        device1 = cursor.fetchone()
        cnx.commit()
        print "here"
        lat2=float(device1[0])
        lon2=float(device1[1])
        device_id = str(device[0])
        lat1=float(device[1])
        lon1=float(device[2])
		#find the distance between the AP and raspberry pi using 'distance fucntion'
        dist=distance(lat1,lat2,lon1,lon2)
        stre = abs(float(a[5]))
		#calculate mui which is the jst the conductivity factor
        mui=(20*log10(float(a[6])*1000)+20*log10(dist)+32.44)/abs(float(a[5]))
		#insert the data into device_data table correspoding the device_id
        readsql = "insert into device_data (channel,strength,pi_id,ap_id,token,mui) values (%d,%f,'%s','%s',%d,%f)"%((int(a[4])),(stre),(pi_id),(device_id),(token),(mui))
        cursor.execute(readsql)
        print "end"
        cnx.commit()
      else :
        #print a[1]
        cursor.execute("select count(mac) from device_info where mac like %s",[a[1]])
        count0 = cursor.fetchone()
        cnx.commit()
		#if the mac is not present in device_info then add it into the device_info and set latitude and longitute to 0 each.
        if(count0[0]!=1):
          readsql = "insert into device_info (mac,essid,frequency,latitude,longitude,device) values ('%s','%s',%f,0,0,1)"%((a[1]),(a[0]),float(a[-1]))
          print readsql
          cursor.execute(readsql)
          cnx.commit()
          print "Inserted"
        
 

# disconnect from server
cnx.close()
