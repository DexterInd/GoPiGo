#!/usr/bin/env python
########################################################################                                                                  
# This example demonstrates using the Ultrasonic sensor with the GoPiGo
#
# In this examples, the GoPiGo keeps reading from the ultrasonic sensor and when it close to the an obstacle, it stops.
#
# http://www.dexterindustries.com/GoPiGo/                                                                
# History
# ------------------------------------------------
# Author     Date      		Comments
# Karan      21 Aug 14 		Initial Authoring
# 			                                                         
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)           
#
########################################################################
#
# ! Attach Ultrasonic sensor to A1 Port.
#
########################################################################
from gopigo import *
import time

distance_to_stop=20		#Distance from obstacle where the GoPiGo should stop
print "Press ENTER to start"
raw_input()				#Wait for input to start
fwd()					#Start moving

while True:
	dist=us_dist(15)			#Find the distance of the object in front
	print "Dist:",dist,'cm'
	if dist<distance_to_stop:	#If the object is closer than the "distance_to_stop" distance, stop the GoPiGo
		print "Stopping"
		stop()					#Stop the GoPiGo
		break
	time.sleep(.1)