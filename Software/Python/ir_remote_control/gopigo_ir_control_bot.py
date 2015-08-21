#!/usr/bin/env python
##################################################
# GoPiGo IR remote control
#
# This example is for controlling the GoPiGo with an Keyes IR remote
# 
# History
# ------------------------------------------------
# Author	Date      		Comments
# Karan		01 June 15	  	Initial Authoring
# Karan 	21 Aug  15		Updated to use LIRC
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)      
##################################################
# Connect the IR receiver to the Serial port on the GoPiGo
# Run the install script before you start
 
import gopigo
import time
import lirc

sockid = lirc.init("keyes", blocking = False)

print "Press any button on the remote to control the GoPiGo"
while True:
	sig= lirc.nextcode()  # press 1 
	if len(sig) !=0:
		print sig[0]

		if sig[0]=="KEY_UP":		#Assign the button with 82 and 83 in position 9 and 10 in the signal to forward command
			print "fwd"
			gopigo.fwd()
		elif sig[0]=="KEY_LEFT":
			print "left"
			gopigo.left()
		elif sig[0]=="KEY_RIGHT":
			print "right"
			gopigo.right()
		elif sig[0]=="KEY_DOWN":
			print "back"
			gopigo.bwd()
		elif sig[0]=="KEY_OK":
			print "Stop"
			gopigo.stop()
	time.sleep(.1)