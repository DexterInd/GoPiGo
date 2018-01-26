#!/usr/bin/env python
#############################################################################################################                                                                  
# Basic example for controlling the GoPiGo using the Keyboard
# Contributed by casten on Gitub https://github.com/DexterInd/GoPiGo/pull/112
#
# This code lets you control the GoPiGo from the VNC or Pi Desktop. Also, these are non-blocking calls so it is much more easier to use too.
#
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
# Karan		27 June 14			Code cleanup                                                    
# Casten	31 Dec  15			Added async io, action until keyup
# Karan		04 Jan	16			Cleaned up the GUI

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
##############################################################################################################

from gopigo import *	#Has the basic functions for controlling the GoPiGo Robot
import sys	#Used for closing the running program
import pygame #Gives access to KEYUP/KEYDOWN events

#Initialization for pygame
pygame.init()
screen = pygame.display.set_mode((700, 400))
pygame.display.set_caption('Remote Control Window')

# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

# Display some text
instructions = '''
                      BASIC GOPIGO CONTROL GUI

This is a basic example for the GoPiGo Robot control 

(Be sure to put focus on thi window to control the gopigo!)

Press:
      ->w: Move GoPiGo Robot forward
      ->a: Turn GoPiGo Robot left
      ->d: Turn GoPiGo Robot right
      ->s: Move GoPiGo Robot backward
      ->t: Increase speed
      ->g: Decrease speed
      ->z: Exit
''';
size_inc=22
index=0
for i in instructions.split('\n'):
	font = pygame.font.Font(None, 36)
	text = font.render(i, 1, (10, 10, 10))
	background.blit(text, (10,10+size_inc*index))
	index+=1

# Blit everything to the screen
screen.blit(background, (0, 0))
pygame.display.flip()

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
