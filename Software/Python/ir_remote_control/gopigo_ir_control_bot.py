#!/usr/bin/env python
##################################################
# GoPiGo IR remote control
#
# This example is for controlling the GoPiGo with an IR remote similar to the one with AC and TV's 
# 
# History
# ------------------------------------------------
# Author	Date      		Comments
# Karan		1 June 15	  	Initial Authoring
#
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)      
##################################################

# Identify the unique strings from the IR_remote test program and use them to control the GoPiGo
# Sample inputs from the remote
# [70, 34, 9, 25, 6, 64, 4, 1, 0, 43, 42, 0, 0, 0, 0, 0, 0, 0, 0, 255]
# [70, 34, 9, 25, 6, 64, 4, 1, 0, 210, 211, 0, 0, 0, 0, 0, 0, 0, 0, 255]
# [70, 34, 9, 25, 6, 64, 4, 1, 0, 82, 83, 0, 0, 0, 0, 0, 0, 0, 0, 255]
# [69, 35, 8, 25, 6, 64, 4, 1, 0, 242, 243, 0, 0, 0, 0, 0, 0, 0, 0, 255]
# [70, 34, 9, 25, 6, 64, 4, 1, 0, 82, 83, 0, 0, 0, 0, 0, 0, 0, 0, 255]
import gopigo
import time

# Assign pin 15 or A1 port to the IR sensor
gopigo.ir_recv_pin(15)
print "Press any button on the remote to control the GoPiGo"

while True:
	ir_data_back=gopigo.ir_read_signal()
	if ir_data_back[0]==-1:		#IO Error
		pass
	elif ir_data_back[0]==0:	#Old signal
		pass
	else:
		sig=ir_data_back[1:]		#Current signal from IR remote
		if sig[9]==82 and sig[10]==83:		#Assign the button with 82 and 83 in position 9 and 10 in the signal to forward command
			print "fwd"
			gopigo.fwd()
		elif sig[9]==114 and sig[10]==115:
			print "left"
			gopigo.left()
		elif sig[9]==242 and sig[10]==243:
			print "right"
			gopigo.right()
		elif sig[9]==210 and sig[10]==211:
			print "back"
			gopigo.bwd()
		elif sig[9]==43 and sig[10]==42:
			print "Stop"
			gopigo.stop()
	time.sleep(.1)