#!/usr/bin/python
###############################################################################################################	
# This library is for using the GoPiGo with Scratch
# http://www.dexterindustries.com/GoPiGo/
# History
# ------------------------------------------------
# Author	 Date	  		Comments
# Karan	  28 July 14  	Initial Authoring
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)		   
# 
# Based on the BrickPi Scratch Library written by Jaikrishna
#
# The Python program acts as the Bridge between Scratch & GoPiGo and must be running for the Scratch program to run.
##############################################################################################################

'''
## License
 GoPiGo for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
 Copyright (C) 2017  Dexter Industries

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
'''

import scratch,sys,threading,math
import re # regular expressions
import os # to handle folder paths
from gopigo import *

try:
	sys.path.insert(0, '/home/pi/Dexter/PivotPi/Software/Scratch/')
	import PivotPiScratch
	pivotpi_available=True
except:
	pivotpi_available=False

defaultCameraFolder="/home/pi/Desktop/"
cameraFolder = defaultCameraFolder

en_gpg=1
en_debug=1
en_ir_sensor=0

	
#360 roation is ~64 encoder pulses
#or 5 deg/pulse
#Deg:Pulse Ratio
DPR = 360.0/64
WHEEL_RAD = 3.25 # Wheels are ~6.5 cm diameter. 
CHASS_WID = 13.5 # Chassis is ~13.5 cm wide.

# Regex patterns
# GET Distance for ultrasonic sensor
# valid commands: GET_DIST, GET DIST, GET_DISTANCE and GET DISTANCE
regexUSsensor = "^GET(\s|_)DIST(ANCE)?"   
comp_regexUSsensor = re.compile(regexUSsensor, re.IGNORECASE)

## This should probably be moved into a gopigo python module.
def cm2pulse(dist):
	'''
	Calculate the number of pulses to move the chassis dist cm.
	pulses = dist * [pulses/revolution]/[dist/revolution]
	'''
	wheel_circ = 2*math.pi*WHEEL_RAD # [cm/rev] cm traveled per revolution of wheel
	#print 'WHEEL_RAD',WHEEL_RAD
	revs = dist/wheel_circ
	#print 'revs',revs
	PPR = 18 # [p/rev] encoder Pulses Per wheel Revolution
	pulses = PPR*revs # [p] encoder pulses required to move dist cm.
	#print 'pulses',pulses
	return pulses

fw_version=fw_ver()
print "GoPiGo Scratch: Current firmware version:",fw_ver()
if fw_version > 1.2:
	pass
else:
	print "GoPiGo Scratch: Please Install the new firmware for the GoPiGo (v1.2+) to use GoPiGo with Scratch. \nPress enter to exit"
	raw_input()
	sys.exit()

try:
	s = scratch.Scratch()
	if s.connected:
		print "GoPiGo Scratch: Connected to Scratch successfully"
	#else:
	#sys.exit(0)
except scratch.ScratchError:
	print "GoPiGo Scratch: Scratch is either not opened or remote sensor connections aren't enabled"
	#sys.exit(0)

class myThread (threading.Thread):	 
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
	def run(self):
		while running:
			time.sleep(.2)			  # sleep for 200 ms

thread1 = myThread(1, "Thread-1", 1)		#Setup and start the thread
thread1.setDaemon(True)

stop()

try:
	s.broadcast('READY')
except NameError:
	print "GoPiGo Scratch: Unable to Broadcast"
while True:
	try:
		m = s.receive()

		while m==None or m[0] == 'sensor-update' :
			m = s.receive()

		msg = m[1]
		if msg.lower() == 'SETUP'.lower() :
			print "GoPiGo Scratch: Setting up sensors done"
		elif msg == 'START' :
			running = True
			if thread1.is_alive() == False:
				thread1.start()
			print "GoPiGo Scratch: Service Started"
		
		# Stop the GoPiGo when "STOP" is received from scratch
		elif msg.lower() == 'STOP'.lower() :
			if en_gpg:
				stop()
			if en_debug:
				print msg
				
		# Move the GoPiGo forward when "FORWARD" is received from scratch
		elif msg[:7].lower()=="FORWARD".lower():
			if en_gpg:
				if len(msg) > 7:
					dist = int(msg[7:])
					pulse = int(cm2pulse(dist))
					enc_tgt(1,1,pulse)
				fwd()
			if en_debug:
				print msg
				
		# Move the GoPiGo back when "BACKWARD" is received from scratch
		elif msg[:8].lower()=="BACKWARD".lower():
			if en_gpg:
				if len(msg) > 8:
					dist = int(msg[8:])
					pulse = int(cm2pulse(dist))
					enc_tgt(1,1,pulse)
				bwd()
			if en_debug:
				print msg
				
		# Turn the GoPiGo left when "LEFT" is received from scratch
		elif msg[:4].lower()=="LEFT".lower():
			if en_gpg:
				if len(msg) > 4:
					deg= int(msg[4:])
					pulse= int(deg/DPR)
					enc_tgt(0,1,pulse)
				left()
			if en_debug:
				print msg
				
		# Turn the GoPiGo right when "RIGHT" is received from scratch
		elif msg[:5].lower()=="RIGHT".lower():
			if en_gpg:
				if len(msg) > 5:
					deg= int(msg[5:])
					pulse= int(deg/DPR)
					enc_tgt(1,0,pulse)
				right()
			if en_debug:
				print msg
				
		# Turn the GoPiGo right when "RIGHT" is received from scratch
		elif msg[:5].lower()=="SPEED".lower():
			if en_gpg:
				speed= int(msg[5:])
				set_speed(speed)
			if en_debug:
				print msg
		# Increase the speed of GoPiGo when "INCREASE SPEED" is received from scratch
		elif msg.lower()=="INCREASE SPEED".lower():
			if en_gpg:
				increase_speed()
			if en_debug:
				print msg
				
		# Decrease the speed of GoPiGo when "DECREASE SPEED" is received from scratch
		elif msg.lower()=="DECREASE SPEED".lower():
			if en_gpg:
				decrease_speed()
			if en_debug:
				print msg
		
		# Turn On or Off the left LED
		elif msg[:4].lower()=="LEDL".lower():
			if en_debug:
				print msg
			l_led_pow=int(msg[4:])
			if en_gpg:
				if l_led_pow > 127:
					led_on(1)
				else:
					led_off(1)
					
		# Turn On or Off the Right LED
		elif msg[:4].lower()=="LEDR".lower():
			if en_debug:
				print msg
			r_led_pow=int(msg[4:])
			if en_gpg:
				if r_led_pow > 127:
					led_on(0)
				else:
					led_off(0)
		elif msg[:9].lower()=="WHEEL ROT".lower():
			if en_debug:
				print msg
			dist= int(msg[9:])
			if en_gpg:
				enc_tgt(1,1,dist)
				
		## Perhaps these should become
		## helper or convenience fcns
		## in the gopigo package.
		## and then below would just reference them.
		elif msg[:3].lower()=="SER".lower():
			if en_debug:
				print msg
			srv_pos=int(msg[3:])
			if en_gpg:
				if srv_pos > 180:
					srv_pos = 180
				elif srv_pos < 0:
					srv_pos = 0
				servo(srv_pos)
				
		# Get distance from the ultrasonic sensor connected to port A1
		#elif msg.lower()=="GET_DIST".lower():
		elif comp_regexUSsensor.match(msg):
			if en_debug:
				print "Received distance request."
				print msg
			dist= us_dist(15)
			if en_gpg:
				s.sensorupdate({'distance':dist})

		# Get value from the light sensor connected to Port A1
		elif msg.lower()=="LIGHT".lower():
			# print "LIGHTS!"
			pin = 1
			mode = "INPUT"
			try:
				a = pinMode(pin, mode)
			except:
				if en_debug:
					e = sys.exc_info()[1]
					print "Error reading light sensor: " + str(e)
			#time.sleep(0.1)
			light = analogRead(pin)
			if en_debug:
				print "Light Reading: " + str(light)
			if en_gpg:
				s.sensorupdate({'light':light})
				
		# Get value from the button connected to the port (A1 or D10) specified in the message
		elif msg[:6].lower()=="BUTTON".lower():
			print "BUTTON!",msg
			try:
				pin = int(msg[6:])
				if pin ==11:
					pin=10
				mode = "OUTPUT"
				a = pinMode(pin, mode)
			except:
				if en_debug:
					e = sys.exc_info()[1]
					print "Error reading button: " + str(e)
			time.sleep(0.1)
			button = digitalRead(pin)
			if en_debug:
				print "Button Reading: " + str(button)
			if en_gpg:
				s.sensorupdate({'button':button})
				
		# Get the value from the sound sensor connected to port A1
		elif msg.lower()=="SOUND".lower():
			pin = 1
			sample = 50
			count = 0
			print "Sound"
			try:
				peak=0
				for j in range(sample):
					analog_read_value=analogRead(pin)
					print ("{}".format(analog_read_value))
					# Print non zero values
					if analog_read_value != 0:
						peak += analog_read_value
						count += 1
	
				avg = peak/(count*2) # the *2 is a leftover from a previous error, kept for backwards compatibility
				print ("avg: {}".format(avg))

			except:
				if en_debug:
					e = sys.exc_info()[1]
					print "Error reading sound sensor: " + str(e)
			if en_debug:
				print "Sound Sensor Reading:(peak,average) ",peak,avg
			if en_gpg:
				s.sensorupdate({'sound':avg})

		# Make sound from the buzzer connected to the D10 port by giving the power value
		elif msg[:6].lower()=="BUZZER".lower():
			print msg
			pin = 10
			try:
				power = int(msg[6:])
				analogWrite(pin,power)
			except:
				if en_debug:
					e = sys.exc_info()[1]
					print "Error with buzzer: " + str(e)
					
		# Set the power in the LED (0-255) connected to port D10
		elif msg[:3].lower()=="LED".lower():
			if en_debug:
				print msg
			led_pow=int(msg[3:])
			pin=10
			if en_gpg:
				analogWrite(pin,led_pow)
				
		# Get the value from the motion sensor connected to Port D10
		elif msg.lower()=="MOTION".lower():
			print "MOTION!"
			pin=10
			try:
				mode = "INPUT"
				a = pinMode(pin, mode)
				time.sleep(0.1)
				motion = digitalRead(pin)
			except:
				if en_debug:
					e = sys.exc_info()[1]
					print "Error reading motion sensor: " + str(e)
			if en_debug:
				print "Motion Reading: " + str(motion)
			if en_gpg:
				s.sensorupdate({'motion':motion})
				
		# Get the value from the IR remote when a button is pressed
		# IR Sensor goes on Serial Port.
		elif msg.lower()=="IR".lower():
			print "IR!"
			if en_ir_sensor==0:
				import ir_receiver
				en_ir_sensor=1
			try:
				a= ir_receiver.nextcode()  # press a button on the remote 
				if len(a) !=0: 
					print a
				else:
					a=[0]	#eturn 0 if no keypress found 
			except:
				if en_debug:
					e = sys.exc_info()[1]
					print "Error reading IR sensor: " + str(a)
			if en_debug:
				print "IR Reading: " + str(a)
			if en_gpg: 
				s.sensorupdate({'ir':a})
				
		# Get the value from the Dexter Industries line sensor
		elif msg.lower()=="LINE".lower():
			try:
				import sys
				sys.path.insert(0, '/home/pi/Dexter/GoPiGo/Software/Python/line_follower')
				# import line_sensor
				import scratch_line
			except ImportError:
				print "Line sensor libraries not found"
				s.sensorupdate({'line':-3})
			if en_debug:
				print "LINE!"
			try:
				line=scratch_line.line_sensor_val_scratch()
			except:
				if en_debug:
					e = sys.exc_info()[1]
					print "Error reading Line sensor: " + str(e)
			if en_debug:
				print "Line Sensor Readings: " + str(line)
			if en_gpg:
				s.sensorupdate({'line':line})	
		
		elif msg.lower()=="READ_IR".lower():
			print "READ_IR!" 
			if en_ir_sensor==0:
				import lirc
				sockid = lirc.init("keyes", blocking = False)
				en_ir_sensor=1
			try:
				read_ir= lirc.nextcode()  # press 1 
				if len(read_ir) !=0:
					print read_ir[0]
			except:
				if en_debug:
					e = sys.exc_info()[1]
					print "Error reading IR sensor: " + str(read_ir)
			if en_debug:
				print "IR Recv Reading: " + str(read_ir)
			if en_gpg:
				if len(read_ir) !=0:
					s.sensorupdate({'read_ir':read_ir[0]})		
				else:
					s.sensorupdate({'read_ir':""})

		# CREATE FOLDER TO SAVE PHOTOS IN

		elif msg[:6].lower()=="FOLDER".lower():
			print "Camera folder"
			try:
				cameraFolder=defaultCameraFolder+str(msg[6:])
				if not os.path.exists(cameraFolder):
					pi=1000  # uid and gid of user pi
					os.makedirs(cameraFolder)
					os.chown(cameraFolder,pi,pi)
					s.sensorupdate({"folder":"created"})
				else:
					s.sensorupdate({"folder":"set"})
			except:
				print "error with folder name"

		# TAKE A PICTURE

		elif msg.lower()=="TAKE_PICTURE".lower():
			print "TAKE_PICTURE" 
			pi=1000  # uid and gid of user pi
			try:
				from subprocess import call
				import datetime
				newimage = "{}/img_{}.jpg".format(cameraFolder,str(datetime.datetime.now()).replace(" ","_",10))
				photo_cmd="raspistill -o {} -w 640 -h 480 -t 1".format(newimage)
				#print photo_cmd
	#				cmd_end=" -w 640 -h 480 -t 1"
	#				dt=str(datetime.datetime.now())
	#				dt=dt.replace(' ','_',10)
				call ([photo_cmd], shell=True)
				os.chown(newimage,pi,pi)
				print "Picture Taken"
				s.sensorupdate({'camera':"Picture Taken"})	
			except:
				if en_debug:
					e = sys.exc_info()[1]
					print "Error taking picture"
				s.sensorupdate({'camera':"Error"})	

					
		elif msg.lower() =="DHT".lower():
			BLUE = 0  # currently only supporting the blue DHT sensor
			if en_debug:
				print "DHT" 
			if en_gpg:
				[dht_temp, dht_humidity] = dht(BLUE)
				if dht_temp == -2.0 or dht_humidity == -2.0:
					print("DHT sensor: bad reading" )
				elif dht_temp == -3.0 or dht_humidity == -3.0:
					print("DHT sensor: not sudo" )
				s.sensorupdate({'temperature':dht_temp})
				s.sensorupdate({'humidity':dht_humidity})

		elif (msg[:5].lower()=="SPEAK".lower()):
			try:
				if en_gpg:
					from subprocess import call
					cmd_beg = "espeak -ven+f1 "
					in_text = msg[len("SPEAK"):]
					cmd_end = " 2>/dev/null"

					call([cmd_beg+"\""+in_text+"\""+cmd_end], shell=True)
				if en_debug:
					print(msg)
			except:
				print("Issue with espeak")

		# PIVOTPI
		elif pivotpi_available==True and PivotPiScratch.isPivotPiMsg(msg):
			pivotsensors = PivotPiScratch.handlePivotPi(msg)
			# print "Back from PivotPi",pivotsensors
			s.sensorupdate(pivotsensors)

								
		else: 
			if en_debug:
				print "Ignoring Command: ", msg
				
		
	except KeyboardInterrupt:
		running= False
		print "GoPiGo Scratch: Disconnected from Scratch"
		break
	except (scratch.scratch.ScratchConnectionError,NameError) as e:
		while True:
			#thread1.join(0)
			print "GoPiGo Scratch: Scratch connection error, Retrying"
			time.sleep(5)
			try:
				s = scratch.Scratch()
				s.broadcast('READY')
				print "GoPiGo Scratch: Connected to Scratch successfully"
				break;
			except scratch.ScratchError:
				print "GoPiGo Scratch: Scratch is either not opened or remote sensor connections aren't enabled\n..............................\n"
	except ValueError as e:
		print e
