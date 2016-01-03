#!/usr/bin/env python
#############################################################################################################                                                                  
# Basic example for controlling the GoPiGo using the Keyboard
# Controls:
# 	w:	Move forward
#	a:	Turn left
#	d:	Turn right
#	s:	Move back
#	x:	Stop
#	t:	Increase speed
#	g:	Decrease speed
#	z: 	Exit
# http://www.dexterindustries.com/GoPiGo/                                                                
# History
# ------------------------------------------------
# Author     	Date      		Comments  
# Karan		27 June 14		Code cleanup                                                    
# Casten		31 Dec  15		Added async io, action until keyup
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
##############################################################################################################

from gopigo import *	#Has the basic functions for controlling the GoPiGo Robot
import sys	#Used for closing the running program
import pygame #Gives access to KEYUP/KEYDOWN events

#Initialization for pygame
pygame.init()
screen = pygame.display.set_mode((300, 60))
pygame.display.set_caption('Remote Control Window')

instructions = '''
This is a basic example for the GoPiGo Robot control 
(Be sure to put focus on Remote Control Window!)
Press:
	w: Move GoPiGo Robot forward
	a: Turn GoPiGo Robot left
	d: Turn GoPiGo Robot right
	s: Move GoPiGo Robot backward
	t: Increase speed
	g: Decrease speed
	z: Exit
''';

print instructions;

while True:
	event = pygame.event.wait();
	if (event.type == pygame.KEYUP):
		stop();
		continue;
	if (event.type != pygame.KEYDOWN):
		continue;	
	char = event.unicode;
	if char=='w':
		fwd()	;# Move forward
	elif char=='a':
		left();	# Turn left
	elif char=='d':
		right();# Turn Right
	elif char=='s':
		bwd();# Move back
	elif char=='t':
		increase_speed();	# Increase speed
	elif char=='g':
		decrease_speed();	# Decrease speed
	elif char=='z':
		print "\nExiting";		# Exit
		sys.exit();
