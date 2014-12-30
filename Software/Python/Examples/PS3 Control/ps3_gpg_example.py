#!/usr/bin/env python
########################################################################                                               
# This example controls the GoPiGo and using a PS3 Dualshock 3 controller
#                                
# http://www.dexterindustries.com/GoPiGo/                                                                
# History
# ------------------------------------------------
# Author     	Date      		Comments
# Karan Nayan   11 July 14		Initial Authoring                                                   
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)           
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
