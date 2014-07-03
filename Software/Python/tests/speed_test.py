from gopigo import *
import sys

while True:
	print "\nCmd:",
	a=raw_input()
	if a=='w':
		fwd()
	elif a=='a':
		set_speed(255)
	elif a=='s':
		set_speed(155)
	elif a=='d':
		disable_encoders()
	time.sleep(.1)