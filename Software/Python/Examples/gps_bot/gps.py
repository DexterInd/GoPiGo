#!/usr/bin/python
import serial, time
import smbus
import math
import RPi.GPIO as GPIO
import struct
import sys
ser = serial.Serial('/dev/ttyAMA0',  9600, timeout = 0)
ser.flush()
class GPS:
	inp=[]
	# Refer to SIM28 NMEA spec file http://www.seeedstudio.com/wiki/images/a/a0/SIM28_DATA_File.zip
	GGA=[]

	def read(self):
		while True:
			GPS.inp=ser.readline()
			if GPS.inp[:6] =='$GPGGA': # GGA data , packet 1
				#print GPS.inp[41:47]
				break
		#print ""
		#print GPS.inp,
		try:
			ind=GPS.inp.index('$GPGGA',5,len(GPS.inp))
			GPS.inp=GPS.inp[ind:]
		except ValueError:
			print ""
		GPS.GGA=GPS.inp.split(",")

		#print GPS.inp
		return [GPS.GGA]
		
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

g=GPS()
f=open("gps_data.csv",'w')
ind=0
while True:
	try:
		x=g.read()
		#print x
		[t,fix,sats,alt,lat,lat_ns,long,long_ew]=g.vals()
		print "Time:",t,"Fix status:",fix,"Sats in view:",sats,"Altitude",alt,"Lat:",lat,lat_ns,"Long:",long,long_ew
		s=str(t)+","+str(float(lat)/100)+","+str(float(long)/100)+"\n"
		f.write(s)
		time.sleep(2)
	except IndexError:
		print "Unable to read"
	except KeyboardInterrupt:
		f.close()
		print "Exiting"
		sys.exit(0)
	
