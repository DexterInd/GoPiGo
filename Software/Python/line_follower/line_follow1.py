#!/usr/bin/env python
# Dexter Industries line sensor python library
#
# This is and example to make the GoPiGo follow the line using the Dexter Industries Line follower
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/
#
# http://www.dexterindustries.com/
'''
## License
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
from __future__ import print_function
from __future__ import division
from builtins import input

# the above lines are meant for Python3 compatibility.
# they force the use of Python3 functionality for print(), 
# the integer division and input()
# mind your parentheses!
import line_sensor
import time
import gopigo
import atexit

atexit.register(gopigo.stop)		# When you ctrl-c out of the code, it stops the gopigo motors.

#Calibrate speed at first run
#100 is good with fresh batteries 
#125 for batteries with half capacity

fwd_speed=110						# Forward speed at which the GoPiGo should run.
									# If you're swinging too hard around your line
									# reduce this speed.
poll_time=0.01						# Time between polling the sensor, seconds.
									
slight_turn_speed=int(.7*fwd_speed)
turn_speed=int(.7*fwd_speed)

last_val=[0]*5						# An array to keep track of the previous values.
curr=[0]*5							# An array to keep track of the current values.

gopigo.set_speed(fwd_speed)

gpg_en=1							#Enable/disable gopigo
msg_en=1							#Enable messages on screen.  Turn this off if you don't want messages.

#Get line parameters
line_pos=[0]*5
white_line=line_sensor.get_white_line()
black_line=line_sensor.get_black_line()
range_sensor= line_sensor.get_range()
threshold=[a+b/2 for a,b in zip(white_line,range_sensor)]	# Make an iterator that aggregates elements from each of the iterables.

#Position to take action on
mid 	=[0,0,1,0,0]	# Middle Position.
mid1	=[0,1,1,1,0]	# Middle Position.
small_l	=[0,1,1,0,0]	# Slightly to the left.
small_l1=[0,1,0,0,0]	# Slightly to the left.
small_r	=[0,0,1,1,0]	# Slightly to the right.
small_r1=[0,0,0,1,0]	# Slightly to the right.
left	=[1,1,0,0,0]	# Slightly to the left.
left1	=[1,0,0,0,0]	# Slightly to the left.
right	=[0,0,0,1,1]	# Sensor reads strongly to the right.
right1	=[0,0,0,0,1]	# Sensor reads strongly to the right.
stop	=[1,1,1,1,1]	# Sensor reads stop.
stop1	=[0,0,0,0,0]	# Sensor reads stop.

#Converts the raw values to absolute 0 and 1 depending on the threshold set
def absolute_line_pos():
	raw_vals=line_sensor.get_sensorval()
	for i in range(5):
		if raw_vals[i]>threshold[i]:
			line_pos[i]=1
		else:
			line_pos[i]=0
	return line_pos
	
#GoPiGo actions
def go_straight():
	if msg_en:
		print("Going straight")
	if gpg_en:
		gopigo.set_speed(fwd_speed)
		gopigo.fwd()
		
def turn_slight_left():
	if msg_en:
		print("Turn slight left")
	if gpg_en:
		gopigo.set_right_speed(slight_turn_speed)
		gopigo.set_left_speed(fwd_speed)
		gopigo.fwd()
		
def turn_left():
	if msg_en:
		print("Turn left")
	if gpg_en:
		gopigo.set_speed(turn_speed)
		gopigo.left()
		
def turn_slight_right():
	if msg_en:
		print("Turn slight right")
	if gpg_en:
		gopigo.set_right_speed(fwd_speed)
		gopigo.set_left_speed(slight_turn_speed)
		gopigo.fwd()

def turn_right():
	if msg_en:
		print("Turn right")
	if gpg_en:
		gopigo.set_speed(turn_speed)
		gopigo.right()
	
def stop_now():
	if msg_en:
		print("Stop")
	if gpg_en:
		gopigo.stop()
		
def go_back():
	if msg_en:
		print("Go Back")
	if gpg_en:
		gopigo.set_speed(turn_speed)
		gopigo.bwd()
	
#Action to run when a line is detected
def run_gpg(curr):
	#if the line is in the middle, keep moving straight
	#if the line is slightly left of right, keep moving straight
	if curr==small_r or curr==small_l or curr==mid or curr==mid1:
		go_straight()
		
	#If the line is towards the sligh left, turn slight right
	elif curr==small_l1:
		turn_slight_right()
	elif curr==left or curr==left1:
		turn_right()
		
	#If the line is towards the sligh right, turn slight left
	elif curr==small_r1:
		turn_slight_left()
	elif curr==right or curr==right1:
		turn_left()
	elif curr==stop: 
		stop_now()
	time.sleep(poll_time)
		
while True:
	last_val=curr
	curr=absolute_line_pos()
	print(curr)
	
	#white line reached
	if curr== stop1:
		if msg_en:
			print("White found, last cmd running")
		for i in range(5):
			run_gpg(last_val)
	else:		
		run_gpg(curr)		
	
