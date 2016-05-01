#!/usr/bin/env python
#
'''
Install dependencies on the command line:
	sudo apt-get install python-lxml
	sudo pip install pykml



'''
# GrovePi Example for using the Grove GPS Module http://www.seeedstudio.com/depot/Grove-GPS-p-959.html?cPath=25_130
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.
#                                                           
# History
# ------------------------------------------------
# Author     Date      		Comments
# Karan      21 Aug 14 		Initial Authoring
# Karan		 10 June 15		Updated the code to reflect the decimal GPS coordinates (contributed by rschmidt on the DI forums: http://www.dexterindustries.com/forum/?topic=gps-example-questions/#post-5668)
import serial, time
import smbus
import math
import RPi.GPIO as GPIO
import struct
import sys
import ir_receiver_check

if ir_receiver_check.check_ir():
	print "Disable IR receiver before continuing"
	exit()
ser = serial.Serial('/dev/ttyAMA0',  9600, timeout = 0)	#Open the serial port at 9600 baud
ser.flush()

class GPS:
	#The GPS module used is a Grove GPS module http://www.seeedstudio.com/depot/Grove-GPS-p-959.html
	inp=[]
	# Refer to SIM28 NMEA spec file http://www.seeedstudio.com/wiki/images/a/a0/SIM28_DATA_File.zip
	GGA=[]

	#Read data from the GPS
	def read(self):	
		while True:
			GPS.inp=ser.readline()
			if GPS.inp[:6] =='$GPGGA': # GGA data , packet 1, has all the data we need
				break
			time.sleep(0.1)     #without the cmd program will crach
		try:
			ind=GPS.inp.index('$GPGGA',5,len(GPS.inp))	#Sometimes multiple GPS data packets come into the stream. Take the data only after the last '$GPGGA' is seen
			GPS.inp=GPS.inp[ind:]
		except ValueError:
			print ""
		GPS.GGA=GPS.inp.split(",")	#Split the stream into individual parts
		return [GPS.GGA]
		
	#Split the data into individual elements
	def vals(self):
		time=GPS.GGA[1]
		lat=GPS.GGA[2]
		lat_ns=GPS.GGA[3]
		long=GPS.GGA[4]
		long_ew=GPS.GGA[5]
		fix=GPS.GGA[6]
		sats=GPS.GGA[7]
		alt=GPS.GGA[9]
		return [time,fix,sats,alt,lat,lat_ns,long,long_ew]
	
	# Convert to decimal degrees
	def decimal_degrees(self, raw_degrees):
		degrees = float(raw_degrees) // 100
		d = float(raw_degrees) % 100 / 60
		return degrees + d

g=GPS()
f=open("gps_data.csv",'w')	#Open file to log the data
f.write("name,latitude,longitude\n")	#Write the header to the top of the file
ind=0


def read_GPS():
	try:
		x=g.read()	#Read from GPS
		[t,fix,sats,alt,lat,lat_ns,long,long_ew]=g.vals()	#Get the individual values
		
		# Convert to decimal degrees
		lat = g.decimal_degrees(float(lat))
		if lat_ns == "S":
			lat = -lat

		long = g.decimal_degrees(float(long))
		if long_ew == "W":
			long = -long
			
		print "Time:",t,"Fix status:",fix,"Sats in view:",sats,"Altitude",alt,"Lat:",lat,lat_ns,"Long:",long,long_ew
		s=str(t)+","+str(float(lat)/100)+","+str(float(long)/100)+"\n"	
		f.write(s)	#Save to file
		# time.sleep(2)

	except IndexError:
		print "Unable to read"
	except KeyboardInterrupt:
		f.close()
		print "Exiting"
		sys.exit(0)

def read_destination_from_file():
	#
	#
	return 0
	
def calculate_azimuth_to_destination(gps_coord_lat, gps_coord_lon, gps_target_coord_lat, gps_target_coord_lon):
	# Calculations were found here:  http://gis.stackexchange.com/questions/108547/how-to-calculate-distance-azimuth-and-dip-from-two-xyz-coordinates
	x1,y1,z1 = 5.0,6.7,1.5
	x2,y2,z2 = 4.0,1.2,1.6
	distance = math.sqrt((x2-x1)**2+(y2-y1)**2+(z2 -z1)**2)
	print distance
	# 5.5910642993977451
	plunge = math.degrees(math.asin((z2-z1)/distance))
	print plunge
	# 1.0248287567800018 # the resulting dip_plunge is positive downward if z2 > z1
	azimuth = math.degrees(math.atan2((x2-x1),(y2-y1)))
	print azimuth
	# -169.69515353123398 # = 360 + azimuth = 190.30484646876602 or  180+ azimuth = 10.304846468766016 over the range of 0 to 360

def calculate_distance_to_destination(gps_coord_lat, gps_coord_lon, gps_target_coord_lat, gps_target_coord_lon):
	# Calculations were found here:  http://gis.stackexchange.com/questions/108547/how-to-calculate-distance-azimuth-and-dip-from-two-xyz-coordinates
	x1,y1,z1 = 5.0,6.7,1.5
	x2,y2,z2 = 4.0,1.2,1.6
	distance = math.sqrt((x2-x1)**2+(y2-y1)**2+(z2 -z1)**2)
	print distance
	
def turn_to_destination():
	return 0

#!/usr/bin/env python
#
'''
Install dependencies on the command line:
	sudo apt-get install python-lxml
	sudo pip install pykml



'''
# GrovePi Example for using the Grove GPS Module http://www.seeedstudio.com/depot/Grove-GPS-p-959.html?cPath=25_130
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.
#                                                           
# History
# ------------------------------------------------
# Author     Date      		Comments
# Karan      21 Aug 14 		Initial Authoring
# Karan		 10 June 15		Updated the code to reflect the decimal GPS coordinates (contributed by rschmidt on the DI forums: http://www.dexterindustries.com/forum/?topic=gps-example-questions/#post-5668)
import serial, time
import smbus
import math
import RPi.GPIO as GPIO
import struct
import sys

ser = serial.Serial('/dev/ttyAMA0',  9600, timeout = 0)	#Open the serial port at 9600 baud
ser.flush()

class GPS:
	#The GPS module used is a Grove GPS module http://www.seeedstudio.com/depot/Grove-GPS-p-959.html
	inp=[]
	# Refer to SIM28 NMEA spec file http://www.seeedstudio.com/wiki/images/a/a0/SIM28_DATA_File.zip
	GGA=[]

	#Read data from the GPS
	def read(self):	
		while True:
			GPS.inp=ser.readline()
			if GPS.inp[:6] =='$GPGGA': # GGA data , packet 1, has all the data we need
				break
			time.sleep(0.1)     #without the cmd program will crach
		try:
			ind=GPS.inp.index('$GPGGA',5,len(GPS.inp))	#Sometimes multiple GPS data packets come into the stream. Take the data only after the last '$GPGGA' is seen
			GPS.inp=GPS.inp[ind:]
		except ValueError:
			print ""
		GPS.GGA=GPS.inp.split(",")	#Split the stream into individual parts
		return [GPS.GGA]
		
	#Split the data into individual elements
	def vals(self):
		time=GPS.GGA[1]
		lat=GPS.GGA[2]
		lat_ns=GPS.GGA[3]
		long=GPS.GGA[4]
		long_ew=GPS.GGA[5]
		fix=GPS.GGA[6]
		sats=GPS.GGA[7]
		alt=GPS.GGA[9]
		return [time,fix,sats,alt,lat,lat_ns,long,long_ew]
	
	# Convert to decimal degrees
	def decimal_degrees(self, raw_degrees):
		degrees = float(raw_degrees) // 100
		d = float(raw_degrees) % 100 / 60
		return degrees + d

g=GPS()
f=open("gps_data.csv",'w')	#Open file to log the data
f.write("name,latitude,longitude\n")	#Write the header to the top of the file
ind=0


def read_GPS():
	try:
		x=g.read()	#Read from GPS
		[t,fix,sats,alt,lat,lat_ns,long,long_ew]=g.vals()	#Get the individual values
		
		# Convert to decimal degrees
		lat = g.decimal_degrees(float(lat))
		if lat_ns == "S":
			lat = -lat

		long = g.decimal_degrees(float(long))
		if long_ew == "W":
			long = -long
			
		print "Time:",t,"Fix status:",fix,"Sats in view:",sats,"Altitude",alt,"Lat:",lat,lat_ns,"Long:",long,long_ew
		s=str(t)+","+str(float(lat)/100)+","+str(float(long)/100)+"\n"	
		f.write(s)	#Save to file
		# time.sleep(2)

	except IndexError:
		print "Unable to read"
	except KeyboardInterrupt:
		f.close()
		print "Exiting"
		sys.exit(0)

def read_destination_from_file():
	#
	#
	return 0
	
def calculate_azimuth_to_destination(gps_coord_lat, gps_coord_lon, gps_target_coord_lat, gps_target_coord_lon):
	# Calculations were found here:  http://gis.stackexchange.com/questions/108547/how-to-calculate-distance-azimuth-and-dip-from-two-xyz-coordinates
	x1,y1,z1 = gps_coord_lat,gps_coord_lon,0
	x2,y2,z2 = gps_target_coord_lat,gps_target_coord_lon,0
	distance = math.sqrt((x2-x1)**2+(y2-y1)**2+(z2 -z1)**2)
	# print distance
	# 5.5910642993977451
	plunge = math.degrees(math.asin((z2-z1)/distance))
	# print plunge
	# 1.0248287567800018 # the resulting dip_plunge is positive downward if z2 > z1
	azimuth = math.degrees(math.atan2((x2-x1),(y2-y1)))
	print azimuth
	# -169.69515353123398 # = 360 + azimuth = 190.30484646876602 or  180+ azimuth = 10.304846468766016 over the range of 0 to 360

def calculate_distance_to_destination(gps_coord_lat, gps_coord_lon, gps_target_coord_lat, gps_target_coord_lon):
	# Calculations were found here:  http://gis.stackexchange.com/questions/108547/how-to-calculate-distance-azimuth-and-dip-from-two-xyz-coordinates
	x1,y1,z1 = gps_coord_lat,gps_coord_lon,0
	x2,y2,z2 = gps_target_coord_lat,gps_target_coord_lon,0
	distance = math.sqrt((x2-x1)**2+(y2-y1)**2+(z2 -z1)**2)
	print distance
	
def turn_to_destination():
	return 0

#Open the CSV of Destinations.
destinations = [10, 9, 8, 7, 6, 5]

for each in destinations:
	print each
	x1,y1,z1 = 5.0,6.7,1.5
	x2,y2,z2 = 4.0,1.2,1.6
	calculate_azimuth_to_destination(x1,y1,x2,y2)
	calculate_distance_to_destination(x1,y1,x2,y2)
	# Read File for destinations
	# For each Destination: 
	# 1. Calculate Azimuth to destination.
	# 2. Calculate distance to destination.  
	# 3. While distance to destination < 3m
	
	#	a. Calculate Azimuth to destination.
	#	b. Calculate distance to destination.  
	#	c. Turn to destination.
	#	d. Run to destination.
	#	e. Wait 5 seconds.  
