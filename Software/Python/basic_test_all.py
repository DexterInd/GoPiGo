#!/usr/bin/env python
from gopigo import *
import sys

import atexit
atexit.register(stop)

while True:
	print "\nCmd:",
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
		print volt(),"V"
	elif a=='b': #servo test
		for i in range(180):
			servo(i)
			print i
			time.sleep(.02)
	elif a=='z':
		sys.exit()
	elif a=='u':
		print us_dist(15),'cm'
	elif a=='l':
		for i in range(256):
			print led(LED_L,i)
			print led(LED_R,i)
			time.sleep(.01)
		print led(LED_L,0)
		print led(LED_R,0)
	elif a=='i':
		motor_fwd()
	elif a=='k':
		motor_bwd()
	elif a=='n':
		left_rot()
	elif a=='m':
		right_rot()
	elif a=='y':
		enc_tgt(1,1,18)
	elif a=='f':
		print "v",fw_ver()
	time.sleep(.1)
