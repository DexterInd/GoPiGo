#!/usr/bin/env python
########################################################################                                               
# This example controls the GoPiGo and using a PS3 Dualshock 3 controller
#                                
# http://www.dexterindustries.com/GoPiGo/                                                                
# History
# ------------------------------------------------
# Author     	Date      		Comments
# Karan Nayan   11 July 14		Initial Authoring                                                   
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
# left,right,up,down to control
# cross to stop
# left joy to turn the camera servo
# l2 to increase speed
# r2 to decrease speed
########################################################################
from ps3 import *		#Import the PS3 library
from gopigo import *	#Import the GoPiGo library

print "Initializing"
p=ps3()		#Create a PS3 object
print "Done"
s=150	#Initialize
run=1
flag=0
while True:
	if run:
		set_speed(s)	#Update the speed
	p.update()			#Read the ps3 values
	if p.up:			#If UP is pressed move forward
		if run:
			fwd()
		print "f"
	elif p.left:		#If LEFT is pressed turn left
		if run:
			left()
			flag=1
		print "l"
	elif p.right:		#If RIGHT is pressed move right
		if run:
			right()
			flag=1
		print "r"
	elif p.down:		#If DOWN is pressed go back
		if run:
			bwd()
		print "b"
	elif p.cross:		#If CROSS is pressed stop
		if run:
			stop()
		print "s"
	else:
		if flag:		#If LEFT or RIGHT key was last pressed start moving forward again 
			fwd()		
			flag=0
	if p.l2:			#Increase the speed if L2 is pressed
		print s
		s+=2
		if s>255:
			s=255
	if p.r2:			#Decrease the speed if R2 is pressed
		print s
		s-=2
		if s<0:
			s=0
	x=(p.a_joystick_left_x+1)*90
	print int(x)
	if run:
		servo(int(x))	#Turn servo a/c to left joy movement
	time.sleep(.01)
