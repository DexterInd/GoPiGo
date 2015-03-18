#!/usr/bin/python
###############################################################################################################                                                               
# This library is for using the GoPiGo with Scratch
# http://www.dexterindustries.com/GoPiGo/                                                                
# History
# ------------------------------------------------
# Author     Date      		Comments
# Karan      28 July 14  	Initial Authoring                                                            
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)           
# 
# Based on the BrickPi Scratch Library written by Jaikrishna
#
# The Python program acts as the Bridge between Scratch & GoPiGo and must be running for the Scratch program to run.
##############################################################################################################

import scratch,sys,threading,math
from gopigo import *

en_gpg=1
en_debug=1
try:
    s = scratch.Scratch()
    if s.connected:
        print "Connected to Scratch successfully"
	#else:
    #sys.exit(0)
except scratch.ScratchError:
    print "Scratch is either not opened or remote sensor connections aren't enabled"
    #sys.exit(0)

class myThread (threading.Thread):     
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        while running:
            time.sleep(.2)              # sleep for 200 ms

thread1 = myThread(1, "Thread-1", 1)        #Setup and start the thread
thread1.setDaemon(True)

stop()
try:
    s.broadcast('READY')
except NameError:
	print "Unable to Broadcast"
while True:
    try:
		m = s.receive()

		while m[0] == 'sensor-update' :
			m = s.receive()

		msg = m[1]
		if msg == 'SETUP' :
			print "Setting up sensors done"
		elif msg == 'START' :
			running = True
			if thread1.is_alive() == False:
				thread1.start()
			print "Service Started"
		elif msg == 'STOP' :
			if en_gpg:
				stop()
			if en_debug:
				print msg
		elif msg=="FORWARD":
			if en_gpg:
				fwd()
			if en_debug:
				print msg
		elif msg=="BACKWARD":
			if en_gpg:
				bwd()
			if en_debug:
				print msg
		elif msg=="LEFT":
			if en_gpg:
				left()
			if en_debug:
				print msg
		elif msg=="RIGHT":
			if en_gpg:
				right()
			if en_debug:
				print msg
		elif msg=="INCREASE SPEED":
			if en_gpg:
				increase_speed()
			if en_debug:
				print msg
		elif msg=="DECREASE SPEED":
			if en_gpg:
				decrease_speed()
			if en_debug:
				print msg
		elif msg[:4]=="LEDL":
			if en_debug:
				print msg
			l_led_pow=int(msg[4:])
			if en_gpg:
				if l_led_pow > 127:
					led_on(1)
				else:
					led_off(1)
				
		elif msg[:4]=="LEDR":
			if en_debug:
				print msg
			r_led_pow=int(msg[4:])
			if en_gpg:
				if en_gpg:
					if r_led_pow > 127:
						led_on(0)
					else:
						led_off(0)
		elif msg[:9]=="WHEEL ROT":
			if en_debug:
				print msg
			dist= int(msg[9:])
			if en_gpg:
				enc_tgt(1,1,dist)
		else:
			if en_debug:
				print "m",msg
				print "Wrong Command"
		
    except KeyboardInterrupt:
        running= False
        print "Disconnected from Scratch"
        break
    except (scratch.scratch.ScratchConnectionError,NameError) as e:
		while True:
			#thread1.join(0)
			print "Scratch connection error, Retrying"
			time.sleep(5)
			try:
				s = scratch.Scratch()
				s.broadcast('READY')
				print "Connected to Scratch successfully"
				break;
			except scratch.ScratchError:
				print "Scratch is either not opened or remote sensor connections aren't enabled\n..............................\n"
