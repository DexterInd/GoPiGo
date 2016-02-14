import line_sensor
import time

poll_time=0.01

# fwd_speed=100
# slight_turn_speed=int(.5*fwd_speed)
# turn_speed=int(.7*fwd_speed)
# poll_time=0.01

last_val=[0]*5
curr=[0]*5

#Enable messages on scree
msg_en=1

#Get line parameters
line_pos=[0]*5
white_line=line_sensor.get_white_line()
black_line=line_sensor.get_black_line()
range_sensor= line_sensor.get_range()
threshold=[a+b/2 for a,b in zip(white_line,range_sensor)]

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

#Converts the raw values to absolute 0 and 1 depending on the threshold set
def absolute_line_pos():
	raw_vals=line_sensor.get_sensorval()
	for i in range(5):
		if raw_vals[i]>threshold[i]:
			line_pos[i]=1
		else:
			line_pos[i]=0
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
