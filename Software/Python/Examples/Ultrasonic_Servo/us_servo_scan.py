#!/usr/bin/env python
############################################################################################                                                                
# This example creates LIDAR like map using an ultrasonic sensor and a servo with the GoPiGo
#                                
# http://www.dexterindustries.com/GoPiGo/                                                                
# History
# ------------------------------------------------
# Author     	Date      		Comments
# Karan		  	13 June 14  	Initial Authoring           
#                                       
'''
## License
 GoPiGo for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
 Copyright (C) 2017  Dexter Industries

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
'''      
#
############################################################################################
#
# ! Attach Ultrasonic sensor to A1 Port.
#
############################################################################################
from gopigo import *
import sys
from collections import Counter
import math

def us_map():
	delay=.02
	debug =0					#True to print all raw values
	num_of_readings=45			#Number of readings to take 
	incr=180/num_of_readings	#increment of angle in servo
	ang_l=[0]*(num_of_readings+1)	#list to hold the angle's of readings
	dist_l=[0]*(num_of_readings+1)	#list to hold the distance at each angle
	x=[0]*(num_of_readings+1)	#list to hold the x coordinate of each point
	y=[0]*(num_of_readings+1)	#list to hold the y coordinate of each point

	buf=[0]*40
	ang=0
	lim=250		#maximum limit of distance measurement (any value over this which be initialized to the limit value)
	index=0
	sample=2	#Number of samples for each angle (more the samples, better the data but more the time taken)
	print "Getting the data"
	
	while True:
		#Take the readings from the Ultrasonic sensor and process them to get the correct values
		for i in range(sample):
			dist=us_dist(15)
			if dist<lim and dist>=0:
				buf[i]=dist
			else:
				buf[i]=lim
		
		#Find the sample that is most common among all the samples for a particular angle
		max=Counter(buf).most_common()	
		rm=-1
		for i in range (len(max)):
			if max[i][0] <> lim and max[i][0] <> 0:
				rm=max[i][0]
				break
		if rm==-1:
			rm=lim
		
		if debug==1:
			print index,ang,rm
		ang_l[index]=ang
		dist_l[index]=rm
		index+=1

		#Move the servo to the next angle
		servo(ang)	
		time.sleep(delay)
		ang+=incr
		#print ang
		if ang>180:
			break
	
	#Print the values in a grid of 51x51 on the terminal
	grid_size=51
	
	#Convert the distance and angle to (x,y) coordinates and scale it down
	for i in range(num_of_readings+1):	
		x[i]=(int(dist_l[i]*math.cos(math.pi*(ang_l[i])/180))/10)
		y[i]=int(dist_l[i]*math.sin(math.pi*ang_l[i]/180))/10
	
	#Rotate the readings so that it is printed in the correct manner
	for i in range(num_of_readings+1):	
		x[i]=(grid_size/2)-x[i]
		y[i]=(grid_size/2)-y[i]

	#Create a grid
	grid = [[0 for a in xrange(grid_size)] for a in xrange(grid_size)] 
	for i in range (num_of_readings+1):
		if dist_l[i]<>lim:
			grid[y[i]][x[i]]=1	
	fence='-'*(grid_size+1)
	
	#Print the map
	print "Map:"
	print fence*2
	for i in range(grid_size/2):
		print "|",
		for j in range (grid_size):
			if (j==grid_size/2)and i==(grid_size/2)-1:
				print 'x',
			elif grid[i][j]==0:
				print ' ',
			else:
				print 'o',
		print "|"
	print fence*2
	return min(dist_l) #Return the closest distance in all directions
	
stop()
while True:
	#GoPiGo moves forward, stops makes a map and again moves forward
	enable_com_timeout(2000)
	enc_tgt(1,1,18)	#Set encoder targetting. Stop after 4 rotations of both the wheels
	fwd()
	time.sleep(.2)
	while True:
		enc=read_enc_status()
		ts=read_timeout_status()
		time.sleep(.05)
		print enc,ts
		if enc == 0:	#Stop when target is reached
			break
		if  ts==0:
			break
		
	time.sleep(2)
	enable_servo()
	if us_map() <20:	#If any obstacle is closer than 20 cm, stop
		break
	disable_servo()