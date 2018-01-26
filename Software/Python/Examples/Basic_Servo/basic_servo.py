#!/usr/bin/env python
########################################################################                                                                  
# This example demonstrates controlling the Servo on the GoPiGo robot.
# In this example, we control the servo with a keyboard.  When you run
# this example from the command line, you'll be prompted for input
# Press a key (a, d, or s) to move the servo.  The data is collected, 
# and sent to the GoPiGo.
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
########################################################################
from gopigo import *

servo_pos=90
print "CONTROLS"
print "a: move servo left"
print "d: move servo right"
print "s: move servo home"
print "Press ENTER to send the commands"

while True:
	#Get the input from the user and change the servo angles
	inp=raw_input()				# Get keyboard input.
	# Now decide what to do with that keyboard input.  
	if inp=='a':
		servo_pos=servo_pos+10	# If input is 'a' move the servo forward 10 degrees.
	elif inp=='d':
		servo_pos=servo_pos-10	# If the input is 'd' move the servo backward by 10 degrees.
	elif inp=='s':
		servo_pos=90			
		
	#Get the servo angles back to the normal 0 to 180 degree range
	if servo_pos>180:
		servo_pos=180
	if servo_pos<0:
		servo_pos=0
		
	servo(servo_pos)		# This function updates the servo with the latest positon.  Move the servo.
	time.sleep(.1)			# Take a break in between operations.  
	