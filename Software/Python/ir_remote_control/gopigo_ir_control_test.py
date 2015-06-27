#!/usr/bin/env python
##################################################
# GoPiGo IR remote control test
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

import gopigo
import time

print gopigo.fw_ver()

gopigo.ir_recv_pin(15)
print "Press any button on the remote to see the data"
while True:
	ir_data_back=gopigo.ir_read_signal()
	if ir_data_back[0]==-1:		#IO Error
		pass
	elif ir_data_back[0]==0:	#Old signal
		pass
	else:
		print ir_data_back[1:]		#Current signal from IR remote
	time.sleep(.1)