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
en_line_sensor=1

if en_line_sensor:
	import line_sensor as l
	
#360 roation is ~64 encoder pulses
#or 5 deg/pulse
#Deg:Pulse Ratio
DPR = 360.0/64
WHEEL_RAD = 3.25 # Wheels are ~6.5 cm diameter. 
CHASS_WID = 13.5 # Chassis is ~13.5 cm wide.

## This should probably be moved into a gopigo python module.
def cm2pulse(dist):
    '''
    Calculate the number of pulses to move the chassis dist cm.
    pulses = dist * [pulses/revolution]/[dist/revolution]
    '''
    wheel_circ = 2*math.pi*WHEEL_RAD # [cm/rev] cm traveled per revolution of wheel
    print 'WHEEL_RAD',WHEEL_RAD
    revs = dist/wheel_circ
    print 'revs',revs
    PPR = 18 # [p/rev] encoder Pulses Per wheel Revolution
    pulses = PPR*revs # [p] encoder pulses required to move dist cm.
    print 'pulses',pulses
    return pulses

fw_version=fw_ver()
print "Current firmware version:",fw_ver()
if fw_version > 1.2:
	pass
else:
	print "Please Install the new firmware for the GoPiGo (v1.2+) to use GoPiGo with Scratch. \nPress enter to exit"
	raw_input()
	sys.exit()

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
		
		# Stop the GoPiGo when "STOP" is received from scratch
		elif msg == 'STOP' :
			if en_gpg:
				stop()
			if en_debug:
				print msg
				
		# Move the GoPiGo forward when "FORWARD" is received from scratch
		elif msg[:7]=="FORWARD":
			if en_gpg:
				if len(msg) > 7:
					dist = int(msg[7:])
					pulse = int(cm2pulse(dist))
					enc_tgt(1,1,pulse)
				fwd()
			if en_debug:
				print msg
				
		# Move the GoPiGo back when "BACKWARD" is received from scratch
		elif msg[:8]=="BACKWARD":
			if en_gpg:
				if len(msg) > 8:
					dist = int(msg[8:])
					pulse = int(cm2pulse(dist))
					enc_tgt(1,1,pulse)
				bwd()
			if en_debug:
				print msg
				
		# Turn the GoPiGo left when "LEFT" is received from scratch
		elif msg[:4]=="LEFT":
			if en_gpg:
				if len(msg) > 4:
					deg= int(msg[4:])
					pulse= int(deg/DPR)
					enc_tgt(0,1,pulse)
				left()
			if en_debug:
				print msg
				
		# Turn the GoPiGo right when "RIGHT" is received from scratch
		elif msg[:5]=="RIGHT":
			if en_gpg:
				if len(msg) > 5:
					deg= int(msg[5:])
					pulse= int(deg/DPR)
					enc_tgt(1,0,pulse)
				right()
			if en_debug:
				print msg
				
		# Turn the GoPiGo right when "RIGHT" is received from scratch
		elif msg[:5]=="SPEED":
			if en_gpg:
				speed= int(msg[5:])
				set_speed(speed)
			if en_debug:
				print msg
		# Increase the speed of GoPiGo when "INCREASE SPEED" is received from scratch
		elif msg=="INCREASE SPEED":
			if en_gpg:
				increase_speed()
			if en_debug:
				print msg
				
		# Decrease the speed of GoPiGo when "DECREASE SPEED" is received from scratch
		elif msg=="DECREASE SPEED":
			if en_gpg:
				decrease_speed()
			if en_debug:
				print msg
		
		# Turn On or Off the left LED
		elif msg[:4]=="LEDL":
			if en_debug:
				print msg
			l_led_pow=int(msg[4:])
			if en_gpg:
				if l_led_pow > 127:
					led_on(1)
				else:
					led_off(1)
					
		# Turn On or Off the Right LED
		elif msg[:4]=="LEDR":
			if en_debug:
				print msg
			r_led_pow=int(msg[4:])
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
				
		## Perhaps these should become
		## helper or convenience fcns
		## in the gopigo package.
		## and then below would just reference them.
		elif msg[:3]=="SER":
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
		elif msg=="GET_DIST":
			if en_debug:
				print "Received distance request."
				print msg
			dist= us_dist(15)
			if en_gpg:
				s.sensorupdate({'distance':dist})

		# Get value from the light sensor connected to Port A1
		elif msg=="LIGHT":
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
		elif msg[:6]=="BUTTON":
			print "BUTTON!",msg
			try:
				pin = int(msg[6:])
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
		# elif msg=="SOUND":
			# # print "LIGHTS!"
			# pin = 1
			# try:
				# sound = analogRead(pin)
			# except:
				# if en_debug:
					# e = sys.exc_info()[1]
					# print "Error reading sound sensor: " + str(e)
			# if en_debug:
				# print "Sound Sensor Reading: " + str(sound)
			# if en_gpg:
				# s.sensorupdate({'sound':sound})
			
		elif msg=="SOUND":
			pin = 1
			print "Sound"
			try:
				d=[]
				i=0
				len=100
				window_size=10
				t=1
				peak=0
				for j in range(t*50):
					analog_read_value=analogRead(1)
					# Print non zero values
					if analog_read_value<>0:
						peak += analog_read_value
	
				avg = peak/(t*100)
				# print avg

			except:
				if en_debug:
					e = sys.exc_info()[1]
					print "Error reading sound sensor: " + str(e)
			if en_debug:
				print "Sound Sensor Reading: ",peak
			if en_gpg:
				s.sensorupdate({'sound':avg})

		# Make sound from the buzzer connected to the D10 port by giving the power value
		elif msg[:6]=="BUZZER":
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
		elif msg[:3]=="LED":
			if en_debug:
				print msg
			led_pow=int(msg[3:])
			pin=10
			if en_gpg:
				analogWrite(pin,led_pow)
				
		# Get the value from the motion sensor connected to Port D10
		elif msg=="MOTION":
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
		# IR Sensor goes on A1 Pin.
		elif msg=="IR":
			print "IR!"
			pin=15
			try:
				#ir_recv_pin(pin)
				time.sleep(0.1)
				ir = ir_read_signal()
			except:
				if en_debug:
					e = sys.exc_info()[1]
					print "Error reading IR sensor: " + str(e)
			if en_debug:
				print "IR Reading: " + str(ir)
			if en_gpg:
				s.sensorupdate({'ir':ir})
				
		# Get the value from the Dexter Industries line sensor
		elif msg=="LINE":
			if en_line_sensor:
				print "LINE!"
				try:
					line=l.line_position()
				except:
					if en_debug:
						e = sys.exc_info()[1]
						print "Error reading Line sensor: " + str(e)
				if en_debug:
					print "Line Sensor Readings: " + str(line)
				if en_gpg:
					s.sensorupdate({'line':line})
					
		elif msg=="SET_BLACK_LINE":
			if en_line_sensor:
				print "SET_BLACK_LINE!"
				try:
					l.set_black_line()
				except:
					if en_debug:
						e = sys.exc_info()[1]
						print "Error reading Line sensor: " + str(l.black_line)
				if en_debug:
					print "Black Line Sensor Readings: " + str(l.black_line)
				if en_gpg:
					s.sensorupdate({'black_line':l.black_line})
		
		elif msg=="SET_WHITE_LINE":
			if en_line_sensor:
				print "SET_WHITE_LINE!"
				try:
					l.set_white_line()
				except:
					if en_debug:
						e = sys.exc_info()[1]
						print "Error reading Line sensor: " + str(l.white_line)
				if en_debug:
					print "White Line Sensor Readings: " + str(l.white_line)
				if en_gpg:
					s.sensorupdate({'white_line':l.white_line})		
					
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
