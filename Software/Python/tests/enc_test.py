from gopigo import *
import sys

while True:
	print "\nCmd:",
	a=raw_input()
	if a=='w':
		fwd()
	elif a=='x':
		stop()
	elif a=='e':
		enable_encoders()
	elif a=='d':
		disable_encoders()
	elif a=='y':
		enc_tgt(1,1,18)
	elif a=='f':
		print "v",fw_ver()
	time.sleep(.1)