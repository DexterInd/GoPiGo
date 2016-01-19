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
