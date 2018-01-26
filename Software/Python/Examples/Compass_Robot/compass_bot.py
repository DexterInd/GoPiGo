#!/usr/bin/env python
##################################################################################################################
# This is a project example for using the GoPiGo with the compass as a turtle robot
#                             
# http://www.dexterindustries.com/GoPiGo      
# Compass module: http://www.seeedstudio.com/depot/Grove-3Axis-Digital-Compass-p-759.html
#                                                       
# History
# ------------------------------------------------
# Author     Date      		Comments
# Karan      22 July 14  	Initial Authoring
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
# Refer to the datasheet to add additional functionality https://www.seeedstudio.com/wiki/images/4/42/HMC5883.pdf
#
# Command:
#	f dist 	:	move forward by "dist" (distance = dist/4 encoder counts. 1 rotation=18 encoder counts) e.g.: f 100
#	l 45	:	rotate left by 45 degrees
#	r 45	:	rotate right by 45 degrees
#
#	NOTE	:	There might be a bug with the Grove Compass which causes it to rotate by more than what you want.
#					Try the compass test to see that you get proper reading when you rotate the compass 360 degrees in
#					Try the compass test to see that you get proper reading when you rotate the compas 360 degrees in
#				90 degree increments.
####################################################################################################################

from grove_compass_lib import *
from gopigo import *
import turtle

en_turtle=1		#Enable turtle graphics
debug=0			#Disable debug mode

if en_turtle:
	turtle.Turtle()
	
c=compass()
divider=4		

set_speed(110)

while True:
	print "CMD:",			#Wait for a command
	cmd=raw_input()
	print cmd
	try:
		if cmd[0]=='f':		#If command is f, move forward by dist/4 encoder counts
			dist=int(cmd[2:])/divider
			enc_tgt(1,1,dist)
			fwd()
			if en_turtle:
				turtle.forward(dist*divider)
				
		elif cmd[0]=='l':	#If command is l, rotate left
			angle=int(cmd[2:])
			if angle >360 or angle <0:
				print "Wrong angle"
				continue
				
			c.update()
			start=360-c.headingDegrees	# compass counts go from 360 -> 0 when turning left, so invert the count
			target= (start+angle)%360	# If target >360 degrees, wrap it to 0
			left_rot()
			while True:
				current=360-c.headingDegrees
				if debug:
					print start,target,current
				if target-start>0:		# Stop when target reached (works when start and target <360
					if current>target:
						right_rot()
						time.sleep(.15)
						stop()
						break;
				else:
					if current>target and current <start-5:	#If target has been wrapped then the check condition changes and keep some tolerence 
						right_rot()
						time.sleep(.15)
						stop()
						break;
				c.update()
				#time.sleep(.1)
			if en_turtle:
				turtle.left(angle)			
				
		elif cmd [0]=='r': 				#Rotate right if command if r
			angle=int(cmd[2:]) 
			if angle >360 or angle <0:
				print "Wrong angle"
				continue
				
			c.update()
			start=c.headingDegrees
			target= (start+angle)%360
			right_rot()
			while True:
				current=c.headingDegrees
				if debug:
					print start,target,current
				if target-start>0:
					if current>target:
						stop()
						break;
				else:
					if current>target and current <start-5:
						stop()
						break;
				c.update()
				#time.sleep(.1)
			if en_turtle:
				turtle.right(angle)
				
		elif cmd[0]=='x':	#Exit on x
			print "Exiting"
			if en_turtle:
				turtle.bye()
			break
			
		elif cmd[0]=='d':	#Show the current reading from the compass
			c.update()
			print c.headingDegrees,360-c.headingDegrees
		else:
			print "Wrong command"
	except ValueError:
		print "Wrong command"
	
	time.sleep(.1)
	#print heading
	
	time.sleep(.1)
	
