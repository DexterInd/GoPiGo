# Karan
# Initial Date: June 13, 2014
#
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)
#
# http://www.dexterindustries.com/
#
# This example is for using the GoPiGo to move around and create a map of the surroundings using an Ultrasonic sensor

from gopigo import *
import sys
from collections import Counter
import math

#Create a map using an ultrasonic sensor and a servo
def us_map():
	delay=.02
	debug =0	#True to spit all raw values
	num_of_readings=45	#Number of readings to take 
	incr=180/num_of_readings	#increment of angle in servo
	ang_l=[0]*(num_of_readings+1)	#list to hold the angle's of readings
	dist_l=[0]*(num_of_readings+1)	#list to hold the distance at each angle
	x=[0]*(num_of_readings+1)	#list to hold the x coordinate of each point
	y=[0]*(num_of_readings+1)	#list to hold the y coordinate of each point

	buf=[0]*40
	ang=0
	lim=250	#limit of distance measurement
	index=0
	sample=2	#Number of samples for each angle
	print "Getting the data"
	while True:
		for i in range(sample):
			dist=us_dist(15)
			if dist<lim and dist>=0:
				buf[i]=dist
			else:
				buf[i]=lim

		max=Counter(buf).most_common()	# Find the most common value among all the samples collected
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

		servo(ang)	#Move the servo to the next angle
		time.sleep(delay)
		ang+=incr
		print ang
		if ang>180:
			break
	
	#Print the values in a grid of 51x51
	grid_size=51
	for i in range(num_of_readings+1):	#Conver the distance and angle to coordinates and scale it down
		x[i]=(int(dist_l[i]*math.cos(math.pi*(ang_l[i])/180))/10)
		y[i]=int(dist_l[i]*math.sin(math.pi*ang_l[i]/180))/10
	for i in range(num_of_readings+1):	#Rotate the readings sow that it is printed in the correct manner
		x[i]=(grid_size/2)-x[i]
		y[i]=(grid_size/2)-y[i]

	grid = [[0 for a in xrange(grid_size)] for a in xrange(grid_size)] 
	for i in range (num_of_readings+1):
		if dist_l[i]<>lim:
			grid[y[i]][x[i]]=1	#Create a grid
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
	
en_slow_i2c()
stop()
while True:
	#enable_encoders()
	enable_com_timeout(1000)
	enc_tgt(1,1,36)	#Set encoder targetting. Stop after 4 rotations of both the wheels
	fwd()
	
	while True:
		if read_status() == 0:	#Stop when target is reached
			break
		time.sleep(1)
	#disable_encoders()
	#enable_servo()
	if us_map() <20:	#If any obstacle is closer than 20 cm, stop
		break
	#disable_servo()