from gopigo import *
disable_servo()
for i in range(180):
	
	servo(i)
	print i
	time.sleep(.01)
	