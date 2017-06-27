# Scratch_Line.  This file adapts the line follower to Scratch.  

import line_sensor
import time
import pickle

poll_time=0.01

# Calibration Files.  These are fixed positions because we assume
# The user is using Raspbian for Robots.
dir_path="/home/pi/Dexter/"
file_b=dir_path+"black_line.txt"
file_w=dir_path+"white_line.txt"
file_r=dir_path+"range_line.txt"

last_val=[0]*5
curr=[0]*5

#Enable messages on screen
msg_en=1

#Get line parameters
line_pos=[0]*5

#Position to take action on
mid 	=[0,0,1,0,0]
mid1	=[0,1,1,1,0]
small_l	=[0,1,1,0,0]
small_l1=[0,1,0,0,0]
small_r	=[0,0,1,1,0]
small_r1=[0,0,0,1,0]
left	=[1,1,0,0,0]
left1	=[1,0,0,0,0]
right	=[0,0,0,1,1]
right1	=[0,0,0,0,1]
stop	=[1,1,1,1,1]
stop1	=[0,0,0,0,0]

def get_black_line():
	global black_line
	#load default values from files
	try:
		with open(file_b, 'rb') as f:
			black_line = pickle.load(f)
	except Exception, e:
		# print e
		black_line=[0]*5
	return black_line

def get_white_line():
	global white_line
	#load default values from files
	try:
		with open(file_w, 'rb') as f:
			white_line = pickle.load(f)
	except Exception, e:
		# print e
		white_line=[0]*5
	return white_line

def get_range():
	global range_col
	#load default values from files
	try:
		with open(file_r, 'rb') as f:
			range_col = pickle.load(f)
	except Exception, e:
		# print e
		range_col=[0]*5
	return range_col

#Converts the raw values to absolute 0 and 1 depending on the threshold set
def absolute_line_pos():

	# line_pos=[0]*5
	# white_line=line_sensor.get_white_line()
	white_line = get_white_line()
	# print "White: " + str(white_line)
	black_line=get_black_line()
	# print "Black: " + str(black_line)
	range_sensor= get_range()
	# print "Range: " + str(range_sensor)
	threshold=[a+b/2 for a,b in zip(white_line,range_sensor)]

	# print "Threshold:" + str(threshold)

	raw_vals=line_sensor.get_sensorval()
	# print (raw_vals)
	
	# updated to handle the case where the line follower is not answering
	for i in range(5):
		if raw_vals[i] == -1:
			line_pos[i] = -1
		elif raw_vals[i]>threshold[i]:
			line_pos[i]=1
		else:
			line_pos[i]=0
			
	# print line_pos
	return line_pos
	
	
#Action to run when a line is detected
def line_sensor_val_scratch():
	# Values returned for the positions in scratch
	# [0,0,1,0,0]	0	# Center
	# [0,1,1,1,0]	0	# Center
	# [0,1,1,0,0]	-1	# Going right
	# [0,1,0,0,0]	-2
	# [1,1,0,0,0]	-3
	# [1,0,0,0,0]	-4	# Completely right
	# [0,0,1,1,0]	1	# Going left
	# [0,0,0,1,0]	2
	# [0,0,0,1,1]	3
	# [0,0,0,0,1]	4	# Completely left
	# [1,1,1,1,1]	5	# All sensors reading black (stopping point)
	# [0,0,0,0,0]	6	# All sensors reading white (has veered off course)
	#				7	# Any thing else (erratic reading)
	curr=absolute_line_pos()
	
	if curr== mid or curr == mid1:
		return 0
	elif curr == small_l:
		return -1	
	elif curr == small_l1:
		return -2
	elif curr == left:
		return -3
	elif curr == left1:
		return -4
	elif curr == small_r:
		return 1	
	elif curr == small_r1:
		return 2
	elif curr == right:
		return 3
	elif curr == right1:
		return 4
	elif curr == stop:
		return 5
	elif curr == stop1:
		return 6
	else:
		return 7
	
def line_sensor_vals():
	#if the line is in the middle, keep moving straight
	#if the line is slightly left of right, keep moving straight
	curr=absolute_line_pos()
	if curr==small_r or curr==small_l or curr==mid or curr==mid1:
		return '0'
		
	#If the line is towards the sligh left, turn slight right
	elif curr==small_l1:
		return '-1'
	elif curr==left or curr==left1:
		return '-2'
		
	#If the line is towards the sligh right, turn slight left
	elif curr==small_r1:
		return '1'
	elif curr==right or curr==right1:
		return '2'
	elif curr==stop: 
		return '3'
	else:
		return '4'
		
		
if __name__ == "__main__":	
	while True:
		print line_sensor_vals()		
		time.sleep(poll_time)
