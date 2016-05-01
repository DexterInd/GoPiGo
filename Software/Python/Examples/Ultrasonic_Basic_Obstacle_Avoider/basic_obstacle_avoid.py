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
'''
## License
 GoPiGo for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
 Copyright (C) 2015  Dexter Industries

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