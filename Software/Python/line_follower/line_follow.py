#!/usr/bin/env python
# Dexter Industries Line sensor Python Library
#
# This is and example to make the GoPiGo follow the line using the Dexter Industries Line follower.
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/
#
# http://www.dexterindustries.com/

import line_sensor
import time
import operator
import gopigo

#Get a value which does have -1
def get_sensorval():
	while True: 
		val=line_sensor.read_sensor()
		if val[0]<>-1:
			return val
		else:
			#Read once more to clear buffer and remove junk values
			val=line_sensor.read_sensor()


#Add a multipler to each sensor
multp=[-100,-50,0,50,100]

#TRAIN for the first time
#reading when all sensors are at white
white=[767,815,859,710,700]
#reading when all sensors are black
black=[1012,1013,1015,1003,1004]
#difference between black and white
range_col=list(map(operator.sub, black, white))

#Calibrate at first run
gopigo.set_speed(150)

gpg_en=1
while True:
	curr=get_sensorval()
	#Get current difference bwtween white and line
	diff_val=list(map(operator.sub, curr, white))

	#find how much black line each sensor is able to get
	#find the position of the bot
	#	-10000 	->	extreme left
	#	0		->	centre
	#	10000	-> 	extreme right
	curr_pos=0
	percent_black_line=[0]*5
	for i in range(5):
		percent_black_line[i]=diff_val[i]*100/range_col[i]
		curr_pos+=percent_black_line[i]*multp[i]
	print curr_pos
	
	if curr_pos <-2500:
		print "r"
		if gpg_en:
			gopigo.set_speed(85)
			gopigo.right()
	elif curr_pos >2500:
		print "l"
		if gpg_en:
			gopigo.set_speed(125)
			gopigo.left()
	else:
		print "f"
		if gpg_en:
			gopigo.set_speed(80)
			gopigo.fwd()
	#time.sleep(.01)
		
		
	
