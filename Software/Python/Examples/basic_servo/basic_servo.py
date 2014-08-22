#!/usr/bin/python
########################################################################                                                                  
# This example is for controlling the Servo on the GoPiGo robot from the keyboard                            
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
from gopigo import *

servo_pos=90
print "CONTROLS"
print "a: move servo left"
print "d: move servo right"
print "s: move servo home"
print "Press ENTER to send the commands"

while True:
	#Get the input from the user and change the servo angles
	inp=raw_input()
	if inp=='a':
		servo_pos=servo_pos+10
	elif inp=='d':
		servo_pos=servo_pos-10
	elif inp=='s':
		servo_pos=90
		
	#Get the servo angles back to the normal 0 to 180 degree range
	if servo_pos>180:
		servo_pos=180
	if servo_pos<0:
		servo_pos=0
		
	servo(servo_pos)#Move the servo
	time.sleep(.1)
	