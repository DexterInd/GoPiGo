#!/usr/bin/env python
########################################################################                                                                  
# This example is for controlling the GoPiGo robot from a mouse scroll                          
# http://www.dexterindustries.com/GoPiGo/                                                                
# History
# ------------------------------------------------
# Author     Date      		Comments
# Karan      20 Aug 14 		Initial Authoring
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
	print x,"\t",y
	
	#If there is a signinficant mouse movement Up (positive y-axis)
	if y >20:
		fwd()	#Move forward

	#If there is a signinficant mouse movement Down (negative y-axis)
	elif y<-20:
		bwd()	#Move Back

	#If there is a signinficant mouse movement Left (positive x-axis)
	elif x<-20:
		left()	#Move left

	#If there is a signinficant mouse movement Right (negative x-axis)
	elif x>20:
		right()	#Move Right

	#Stop the GoPiGo if left mouse button pressed
	if l:
		stop()
	time.sleep(.01)
