#!/usr/bin/env python
########################################################################                                                                  
# This example is for controlling the GoPiGo robot from a mouse buttons                        
# http://www.dexterindustries.com/GoPiGo/                                                                
# History
# ------------------------------------------------
# Author     Date      		Comments
# Karan      13 June 14 	Initial Authoring
# 			                                                         
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)           
#
########################################################################
import struct
import sys
from gopigo import *

#Open the stream of data coming from the mouse
file = open( "/dev/input/mice", "rb" );
speed=150

debug = 0	#Print raw values when debugging

#Parse through the fata coming from mouse
#Returns: 	[left button pressed,
#		middle button pressed,
#		right button pressed,
#		change of position in x-axis,
#		change of position in y-axis]
def getMouseEvent():
	buf = file.read(3)
	button = ord( buf[0] )
	bLeft = button & 0x1
	bMiddle = ( button & 0x4 ) > 0
	bRight = ( button & 0x2 ) > 0
	x,y = struct.unpack( "bb", buf[1:] )
	if debug:
		print ("L:%d, M: %d, R: %d, x: %d, y: %d\n" % (bLeft,bMiddle,bRight, x, y) )
	return [bLeft,bMiddle,bRight,x,y]
	
flag=0
print "Press Enter to start"
a=raw_input()	#Wait for an input to start
set_speed(speed)
stop()
while( 1 ):
	[l,m,r,x,y]=getMouseEvent()	#Get the inputs from the mouse
	if debug:
		print l,m,r,x,y
		
	if flag==1: #If left or right mouse not pressed, move forward
		fwd()
		flag=0
	if l:		#If left mouse buton pressed, turn left
		left()
		flag=1
	if m:		#If middle mouse button pressed, stop
		stop()
	if r:		#If right mouse button presses, turn right
		right()
		flag=1
	if l and r:	#If both the left and right mouse buttons pressed, go back
		bwd()
