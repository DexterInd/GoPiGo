#!/usr/bin/env python
########################################################################                                               
# This is the library to read values from PS3 Dualshock 3 controller
#                                
# http://www.dexterindustries.com/GoPiGo/                                                                
# History
# ------------------------------------------------
# Author     	Date      		Comments
# Karan Nayan   11 July 14		Initial Authoring                                                   
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)           
#
# Dependencies- pygame
# Pairing the controller using bluetooth
# http://booting-rpi.blogspot.ro/2012/08/dualshock-3-and-raspberry-pi.html
# PS3 Key configuration http://wiki.ros.org/ps3joy
# 
# Key values can be obtained by creating a ps3 object and calling update() regularly
########################################################################
import pygame, sys, time ,os
from pygame.locals import *

#PS3 functions and variables
class ps3:
	joystick=0
	joystick_count=0
	numaxes=0
	numbuttons=0
	#left=right=up=down=l1=l2=r1=r2=triangle=circle=square=cross=select=start=ps=joystick_left=joystick_right=0
	#a_left=a_right=a_up=a_down=a_l1=a_l2=a_r1=a_r2=a_triangle=a_circle=a_square=a_cross=a_select=a_start=a_ps=a_joystick_left_x=a_joystick_left_y=a_joystick_right_x=a_joystick_right_y=acc_x=acc_y=acc_z=gyro_yaw=0
	
	#Initialize the controller when the oject is created
	def __init__(self):
		#Make the stdout buffer as 0,because of bug in Pygame which keeps on printing debug statements
		#http://stackoverflow.com/questions/107705/python-output-buffering
		sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
		
		pygame.init()
		pygame.joystick.init()
		ps3.joystick = pygame.joystick.Joystick(0)
		ps3.joystick.init()
		ps3.joystick_count = pygame.joystick.get_count()
		ps3.numaxes = ps3.joystick.get_numaxes()
		ps3.numbuttons = ps3.joystick.get_numbuttons()
		# get count of joysticks=1, axes=27, buttons=19 for DualShock 3
	
	#Update the button values
	def update(self):
		loopQuit = False
		button_state=[0]*self.numbuttons
		button_analog=[0]*self.numaxes
		#while loopQuit == False:
		outstr = ""
		
		#Start suppressing the output on stdout from Pygame
		devnull = open('/dev/null', 'w')
		oldstdout_fno = os.dup(sys.stdout.fileno())
		os.dup2(devnull.fileno(), 1)
		
		#Read analog values
		for i in range(0,self.numaxes):
			button_analog[i] = self.joystick.get_axis(i)
		
		#a_left				=button_analog[]
		self.a_right				=button_analog[9]
		self.a_up				=button_analog[8]
		self.a_down				=button_analog[10]
		self.a_l1				=button_analog[14]
		self.a_l2				=button_analog[12]
		self.a_r1				=button_analog[15]
		self.a_r2				=button_analog[13]
		self.a_triangle			=button_analog[16]
		self.a_circle			=button_analog[17]
		self.a_square			=button_analog[19]
		self.a_cross				=button_analog[18]

		self.a_joystick_left_x	=button_analog[0]
		self.a_joystick_left_y	=button_analog[1]
		self.a_joystick_right_x	=button_analog[2]
		self.a_joystick_right_y	=button_analog[3]
		self.acc_x				=button_analog[23]
		self.acc_y				=button_analog[24]
		self.acc_z				=button_analog[25]
		
		#Read digital values
		for i in range(0,self.numbuttons):
			button_state[i]=self.joystick.get_button(i)
		self.select			=button_state[0]
		self.joystick_left	=button_state[1]
		self.joystick_right	=button_state[2]
		self.start			=button_state[3]
		self.up				=button_state[4]
		self.right			=button_state[5]
		self.down			=button_state[6]
		self.left			=button_state[7]
		self.l2				=button_state[8]
		self.r2				=button_state[9]
		self.l1				=button_state[10]
		self.r1				=button_state[11]
		self.triangle		=button_state[12]
		self.circle			=button_state[13]
		self.cross			=button_state[14]
		self.square			=button_state[15]
		self.ps				=button_state[16]
		
		#Enable output on stdout
		os.dup2(oldstdout_fno, 1)	
		os.close(oldstdout_fno)
		
		#refresh
		pygame.event.get()
		return button_analog
	
