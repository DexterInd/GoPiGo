from gopigo import *
while True:
	a=raw_input()
	if a=='w':
		fwd()
	elif a=='a':
		left()
	elif a=='d':
		right()
	elif a=='s':
		bwd()
	elif a=='x':
		stop()
	elif a=='t':
		increase_speed()
	elif a=='g':
		decrease_speed()
	elif a=='v':
		print volt(),'V'
	elif a=='u':
		print us_dist(17)
	elif a=='b': #servo test
		for i in range(180):
			servo(i)
			time.sleep(.02)
	time.sleep(.1)