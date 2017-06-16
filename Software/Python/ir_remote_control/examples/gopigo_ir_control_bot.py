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
# Karan		06 Oct  16		Updated to use DI library with noise removal
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2015  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
##################################################
# Connect the IR receiver to the Serial port on the GoPiGo
# Run the install script before you start
 
import gopigo
import time,sys
import ir_receiver


print "Press any button on the remote to control the GoPiGo"
while True:
	sig= inp= ir_receiver.nextcode() 
	if len(sig) !=0:
		print sig
		if sig=="KEY_UP":		#Assign the button with 82 and 83 in position 9 and 10 in the signal to forward command
			print "fwd"
			gopigo.fwd()
		elif sig=="KEY_LEFT":
			print "left"
			gopigo.left()
		elif sig=="KEY_RIGHT":
			print "right"
			gopigo.right()
		elif sig=="KEY_DOWN":
			print "back"
			gopigo.bwd()
		elif sig=="KEY_OK":
			print "Stop"
			gopigo.stop()
	time.sleep(.1)
