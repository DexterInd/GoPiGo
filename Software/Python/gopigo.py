#!/usr/bin/env python
from __future__ import print_function
from __future__ import division
# the above lines are meant for Python3 compatibility.
# they force the use of Python3 functionality for print()
# and the integer division
# mind your parentheses!

########################################################################
# This library is used for communicating with the GoPiGo.
# http://www.dexterindustries.com/GoPiGo/
# History
# ------------------------------------------------
# Author	Date      		Comments
# Karan		30 March 14  	Initial Authoring
# 			02 July  14		Removed bugs and some features added (v0.9)
#			26 Aug	 14		Code commenting and cleanup
#			07 June  16		DHT example added
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
#
########################################################################

import sys
import time
import math
import struct
import di_i2c

WHEEL_RAD=3.25
WHEEL_CIRC=2*math.pi*WHEEL_RAD
PPR = 18 # encoder Pulses Per Revolution

def set_bus(bus):
	global i2c
	i2c = di_i2c.DI_I2C(bus = bus, address = address)

address = 0x08
set_bus("RPI_1SW")

#GoPiGo Commands
fwd_cmd				=[119]		#Move forward with PID
motor_fwd_cmd		=[105]		#Move forward without PID
bwd_cmd				=[115]		#Move back with PID
motor_bwd_cmd		=[107]		#Move back without PID
left_cmd			=[97]		#Turn Left by turning off one motor
left_rot_cmd		=[98]		#Rotate left by running both motors is opposite direction
right_cmd			=[100]		#Turn Right by turning off one motor
right_rot_cmd		=[110]		#Rotate Right by running both motors is opposite direction
stop_cmd			=[120]		#Stop the GoPiGo
ispd_cmd			=[116]		#Increase the speed by 10
dspd_cmd			=[103]		#Decrease the speed by 10
m1_cmd      		=[111]     	#Control motor1
m2_cmd    			=[112]     	#Control motor2
read_motor_speed_cmd=[114]		#Get motor speed back

volt_cmd			=[118]		#Read the voltage of the batteries
us_cmd				=[117]		#Read the distance from the ultrasonic sensor
led_cmd				=[108]		#Turn On/Off the LED's
servo_cmd			=[101]		#Rotate the servo
enc_tgt_cmd			=[50]		#Set the encoder targeting
fw_ver_cmd			=[20]		#Read the firmware version
en_enc_cmd			=[51]		#Enable the encoders
dis_enc_cmd			=[52]		#Disable the encoders
read_enc_status_cmd	=[53]		#Read encoder status
en_servo_cmd		=[61]		#Enable the servo's
dis_servo_cmd		=[60]		#Disable the servo's
set_left_speed_cmd	=[70]		#Set the speed of the right motor
set_right_speed_cmd	=[71]		#Set the speed of the left motor
en_com_timeout_cmd	=[80]		#Enable communication timeout
dis_com_timeout_cmd	=[81]		#Disable communication timeout
timeout_status_cmd	=[82]		#Read the timeout status
enc_read_cmd		=[53]		#Read encoder values
trim_test_cmd		=[30]		#Test the trim values
trim_write_cmd		=[31]		#Write the trim values
trim_read_cmd		=[32]

digital_write_cmd   =[12]      	#Digital write on a port
digital_read_cmd    =[13]      	#Digital read on a port
analog_read_cmd     =[14]      	#Analog read on a port
analog_write_cmd    =[15]      	#Analog read on a port
pin_mode_cmd        =[16]      	#Set up the pin mode on a port

ir_read_cmd			=[21]
ir_recv_pin_cmd		=[22]
cpu_speed_cmd		=[25]

#LED Pins
#MAKE COMPATIBLE WITH OLD FIRMWARE
# LED_L_PIN=17
# LED_R_PIN=16

#port definition
analogPort=15
digitalPort=10

#LED setup
LED_L=1
LED_R=0

# This allows us to be more specific about which commands contain unused bytes
unused = 0

v16_thresh=790
version = 0
debug=0

#Write I2C block
def write_i2c_block(command, block):
	try:
		op = i2c.write_reg_list(command[0], block)
		time.sleep(.005)
		return op
	except IOError:
		if debug:
			print ("IOError")
		return -1
	return 1

#Write a byte to the GoPiGo
def writeNumber(value):
	try:
		i2c.write_8(value)
		time.sleep(.005)
	except IOError:
		if debug:
			print ("IOError")
		return -1
	return 1

#Read a byte from the GoPiGo
def readByte():
	try:
		number = i2c.read_8()
		time.sleep(.005)
	except IOError:
		if debug:
			print ("IOError")
		return -1
	return number

#Control Motor 1
def motor1(direction,speed):
	return write_i2c_block(m1_cmd, [direction,speed,0])

#Control Motor 2
def motor2(direction,speed):
	return write_i2c_block(m2_cmd, [direction,speed,0])

#Move the GoPiGo forward
def fwd(dist=0): #distance is in cm
	"""
	Starts moving the GoPiGo forward at the currently set motor speeds.

	Takes an optional parameter to indicate a specific distance to move
	forward. If not given, negative, or zero then it will move forward until
	another direction or stop function is called.

	Returns -1 if the action fails.

	:param int dist: The distance in cm to move forward.
	:return: A value indicating if the action suceeded.
	:rtype: int
	"""
	try:
		if dist>0:
			# this casting to int doesn't seem necessary
			pulse=int(PPR*(dist//WHEEL_CIRC) )
			enc_tgt(1,1,pulse)
	except Exception as e:
		print ("gopigo fwd: {}".format(e))
		pass
	return write_i2c_block(motor_fwd_cmd, [0,0,0])

# support more explicit spelling for forward function
forward=fwd

#Move the GoPiGo forward without PID
def motor_fwd():
	return write_i2c_block(motor_fwd_cmd, [0,0,0])

#Move GoPiGo back
def bwd(dist=0):
	"""
	Starts moving the GoPiGo backward at the currently set motor speeds.

	Takes an optional parameter to indicate a specific distance to move
	backward. If not given, negative, or zero then it will move backward
	until another direction or stop function is called.

	Returns -1 if the action fails.

	:param int dist: The distance in cm to move backward.
	:return: A value indicating if the action suceeded.
	:rtype: int
	"""
	try:
		if dist>0:
			# this casting to int doesn't seem necessary
			pulse=int(PPR*(dist//WHEEL_CIRC) )
			enc_tgt(1,1,pulse)
	except Exception as e:
		print ("gopigo bwd: {}".format(e))
		pass
	return write_i2c_block(motor_bwd_cmd, [0,0,0])

# support more explicit spelling for backward function
backward=bwd

#Move GoPiGo back without PID control
def motor_bwd():
	return write_i2c_block(motor_bwd_cmd, [0,0,0])

#Turn GoPiGo Left slow (one motor off, better control)
def left():
	return write_i2c_block(left_cmd, [0,0,0])

#Rotate GoPiGo left in same position (both motors moving in the opposite direction)
def left_rot():
	return write_i2c_block(left_rot_cmd, [0,0,0])

#Turn GoPiGo right slow (one motor off, better control)
def right():
	return write_i2c_block(right_cmd, [0,0,0])

#Rotate GoPiGo right in same position both motors moving in the opposite direction)
def right_rot():
	return write_i2c_block(right_rot_cmd, [0,0,0])

DPR = 360.0/64
# turn x degrees to the right
def turn_right(degrees):
	pulse = int(degrees//DPR)
	enc_tgt(1,0,pulse)
	right()

def turn_right_wait_for_completion(degrees):
	'''
	Same as turn_right() but blocking
	'''
	turn_right(degrees)
	pulse = int(degrees//DPR)
	while enc_read(0) < pulse:
		pass


# turn x degrees to the left
def turn_left(degrees):
	pulse = int(degrees//DPR)
	enc_tgt(0,1,pulse)
	left()

def turn_left_wait_for_completion(degrees):
	'''
	same as turn_left() but blocking.
	'''
	turn_left(degrees)
	pulse = int(degrees//DPR)
	while enc_read(1) < pulse:
		pass


#Stop the GoPiGo
def stop():
	"""
	Brings the GoPiGo to a full stop.

	Returns -1 if the action fails.

	:return: A value indicating if the action suceeded.
	:rtype: int
	"""
	return write_i2c_block(stop_cmd, [0,0,0])

#Increase the speed
def increase_speed():
	return write_i2c_block(ispd_cmd, [0,0,0])

#Decrease the speed
def decrease_speed():
	return write_i2c_block(dspd_cmd, [0,0,0])

#Trim test with the value specified
def trim_test(value):
	if value>100:
		value=100
	elif value<-100:
		value=-100
	value+=100
	write_i2c_block(trim_test_cmd, [value,0,0])

#Read the trim value in	EEPROM if present else return -3
def trim_read():
	write_i2c_block(trim_read_cmd, [0,0,0])
	time.sleep(.08)
	try:
		b1=i2c.read_8()
		b2=i2c.read_8()
	except IOError:
		return -1

	if b1!=-1 and b2!=-1:
		v=b1*256+b2
		if v==255:
			return -3
		return v
	else:
		return -1

#Write the trim value to EEPROM, where -100=0 and 100=200
def trim_write(value):
	if value>100:
		value=100
	elif value<-100:
		value=-100
	value+=100
	write_i2c_block(trim_write_cmd, [value,0,0])


# Arduino Digital Read
def digitalRead(pin):
	if pin ==10 or pin ==15 or pin ==0 or pin ==1:
		write_i2c_block(digital_read_cmd, [pin, unused, unused])
		time.sleep(.1)
		n=i2c.read_8()
		i2c.read_8()		#Empty the buffer
		return n
	else:
		return -2

# Arduino Digital Write
def digitalWrite(pin, value):
	#if pin ==10 or pin ==0 or pin ==1 or pin==5 or pin ==16 or pin==17 :
	if value==0 or value ==1:
		write_i2c_block(digital_write_cmd, [pin, value, unused])
		# time.sleep(.005)	#Wait for 5 ms for the commands to complete
		return 1
	#else:
	#	return -2

# Setting Up Pin mode on Arduino
def pinMode(pin, mode):
	# if pin ==10 or pin ==15 or pin ==0 or pin ==1:
	if mode == "OUTPUT":
		write_i2c_block(pin_mode_cmd, [pin, 1, unused])
	elif mode == "INPUT":
		write_i2c_block(pin_mode_cmd, [pin, 0, unused])
	#time.sleep(.005)	#Wait for 5 ms for the commands to complete
	return 1
	# else:
		# return -2

# Read analog value from Pin
def analogRead(pin):
	#if pin == 1 :
	write_i2c_block(analog_read_cmd, [pin, unused, unused])
	time.sleep(.007)
	try:
		b1=i2c.read_8()
		b2=i2c.read_8()
	except IOError:
		return -1
	return b1* 256 + b2
	#else:
	#	return -2

# Write PWM
def analogWrite(pin, value):
	if pin == 10 :
		write_i2c_block(analog_write_cmd, [pin, value, unused])
		return 1
	else:
		return -2

#Read voltage
#	return:	voltage in V
def volt():
	write_i2c_block(volt_cmd, [0,0,0])
	time.sleep(.1)
	try:
		b1=i2c.read_8()
		b2=i2c.read_8()
	except IOError:
		return -1

	if b1!=-1 and b2!=-1:
		v=b1*256+b2
		v=(5*float(v)/1024)/0.4
		return round(v,2)
	else:
		return -1

#Read board revision
#	return:	voltage in V
def brd_rev():
	write_i2c_block(analog_read_cmd, [7, unused, unused])
	time.sleep(.1)
	try:
		b1=i2c.read_8()
		b2=i2c.read_8()
	except IOError:
		return -1
	return b1* 256 + b2

#Read ultrasonic sensor
#	arg:
#		pin -> 	Pin number on which the US sensor is connected
#	return:		distance in cm
def us_dist(pin):
	"""
	Reads the distance measured by the ultrasonic sensor.

	The pin for the ultrasonic sensor should be pin 15 (Analog Port A1).

	>>> us_dist(15)
	42

	If the reading from the ultrasonic sensor fails, then the function call
	will return -1.

	If this function does not seem to be working properly, then make sure that
	your ultrasonic sensor is plugged into the Analog Port A1.

	See the following link for more information on the GoPiGo ports:

	https://www.dexterindustries.com/GoPiGo/learning/hardware-port-description/

	:param int pin: The pin that the ultrasonic sensor is conected to.
	:return: The distance in cm measured by the ultrasonic sensor.
	:rtype: int
	"""
	write_i2c_block(us_cmd, [pin,0,0])
	time.sleep(.08)
	try:
		b1=i2c.read_8()
		b2=i2c.read_8()
	except IOError:
		return -1
	if b1!=-1 and b2!=-1:
		v=b1*256+b2
		return v
	else:
		return -1

def corrected_us_dist(pin):
	'''
	based on lab experiments, the US sensor has to be corrected
	with the following equation:
		(x+4.41)/1.423
	This seems to give the best results for the sensors on hand
	'''
	raw_data = float(us_dist(pin))

	if raw_data > 0:
		corrected_data = (raw_data + 4.41)  / 1.423
	else:
		corrected_data = raw_data
	# print(raw_data,corrected_data)
	return int(corrected_data)

def read_motor_speed():
	write_i2c_block(read_motor_speed_cmd, [unused,unused,unused])
	try:
		s1=i2c.read_8()
		s2=i2c.read_8()
	except IOError:
		return [-1,-1]
	return [s1,s2]


#Turn led on
#	arg:
#		l_id: 1 for left LED and 0 for right LED
def led_on(l_id):
	if check_version() > 14:
		r_led=16
		l_led=17
	else:
		r_led=5
		l_led=10

	if l_id==LED_L or l_id==LED_R:
		if l_id==LED_L:
			pinMode(l_led,"OUTPUT")
			digitalWrite(l_led,1)
		elif l_id==LED_R:
			pinMode(r_led,"OUTPUT")
			digitalWrite(r_led,1)
		return 1
	else:
		return -1

#Turn led off
#	arg:
#		l_id: 1 for left LED and 0 for right LED
def led_off(l_id):
	if check_version()>14:
		r_led=16
		l_led=17
	else:
		r_led=5
		l_led=10

	if l_id==LED_L or l_id==LED_R:
		if l_id==LED_L:
			pinMode(l_led,"OUTPUT")
			digitalWrite(l_led,0)
		elif l_id==LED_R:
			pinMode(r_led,"OUTPUT")
			digitalWrite(r_led,0)
		return 1
	else:
		return -1

#Set servo position
#	arg:
#		position: angle in degrees to set the servo at
def servo(position):
	write_i2c_block(servo_cmd, [position,0,0])
	#time.sleep(.05)

#Set encoder targeting on
#arg:
#	m1: 0 to disable targeting for m1, 1 to enable it
#	m2:	1 to disable targeting for m2, 1 to enable it
#	target: number of encoder pulses to target (18 per revolution)
def enc_tgt(m1,m2,target):
#	print("enc_tgt m1 {} m2 {} target {}".format(m1,m2,target))
	if m1>1 or m1<0 or m2>1 or m2<0:
		return -1
	m_sel=m1*2+m2
	write_i2c_block(enc_tgt_cmd, [m_sel,target//256,target%256])
	return 1

#Read encoder value
#	arg:
#		motor -> 	0 for motor1 and 1 for motor2
#	return:		distance in cm
def enc_read(motor):
	write_i2c_block(enc_read_cmd, [motor,0,0])
	time.sleep(.08)
	try:
		b1=i2c.read_8()
		b2=i2c.read_8()
	except IOError:
		return -1
	if b1!=-1 and b2!=-1:
		v=b1*256+b2
		return v
	else:
		return -1

#Returns the firmware version
def fw_ver():
	write_i2c_block(fw_ver_cmd, [0,0,0])
	time.sleep(.1)
	try:
		ver=i2c.read_8()
		i2c.read_8()		#Empty the buffer
	except IOError:
		return -1
	return float(ver)/10

#Enable the encoders (enabled by default)
def enable_encoders():
	return write_i2c_block(en_enc_cmd, [0,0,0])

#Disable the encoders (use this if you don't want to use the encoders)
def disable_encoders():
	return write_i2c_block(dis_enc_cmd, [0,0,0])

#Enables the servo
def enable_servo():
	return write_i2c_block(en_servo_cmd, [0,0,0])

#Disable the servo
def disable_servo():
	return write_i2c_block(dis_servo_cmd, [0,0,0])

#Set speed of the left motor
#	arg:
#		speed-> 0-255
def set_left_speed(speed):
	"""
	Sets the speed of the left motor. The speed should be in the range of
	[0, 255].

	Returns -1 if the motor speed change fails.

	:param int speed: The speed to set the left motor to. [0, 255]
	:return: A value indicating if the setting suceeded.
	:rtype: int
	"""
	if speed >255:
		speed =255
	elif speed <0:
		speed =0
	return write_i2c_block(set_left_speed_cmd, [speed,0,0])

#Set speed of the right motor
#	arg:
#		speed-> 0-255
def set_right_speed(speed):
	"""
	Sets the speed of the right motor. The speed should be in the range of
	[0, 255].

	Returns -1 if the motor speed change fails.

	:param int speed: The speed to set the right motor to. [0, 255]
	:return: A value indicating if the setting suceeded.
	:rtype: int
	"""
	if speed >255:
		speed =255
	elif speed <0:
		speed =0
	return write_i2c_block(set_right_speed_cmd, [speed,0,0])

#Set speed of the both motors
#	arg:
#		speed-> 0-255
def set_speed(speed):
	"""
	Sets the speed of the left and right motors to the given speed. The speed
	should be in the range of [0, 255].

	Sleeps for 0.1 seconds in between setting the left and right motor speeds.

	:param int speed: The speed to set the motors to. [0, 255]
	"""
	if speed >255:
		speed =255
	elif speed <0:
		speed =0
	set_left_speed(speed)
	time.sleep(.1)
	set_right_speed(speed)

#Enable communication time-out(stop the motors if no command received in the specified time-out)
#	arg:
#		timeout-> 0-65535 (timeout in ms)
def enable_com_timeout(timeout):
	return write_i2c_block(en_com_timeout_cmd, [timeout//256,timeout%256,0])

#Disable communication time-out
def disable_com_timeout():
	return write_i2c_block(dis_com_timeout_cmd, [0,0,0])

#Read the status register on the GoPiGo
#	Gets a byte, 	b0-enc_status
#					b1-timeout_status
#	Return:	list with 	l[0]-enc_status
#						l[1]-timeout_status
def read_status():
	st=i2c.read_8()
	st_reg=[st & (1 <<0),(st & (1 <<1))//2]
	return st_reg

#Read encoder status
#	return:	0 if encoder target is reached

def read_enc_status():
	st=read_status()
	return st[0]

#Read timeout status
#	return:	0 if timeout is reached
def read_timeout_status():
	st=read_status()
	return st[1]

# Grove - Infrared Receiver- get the commands received from the Grove IR sensor
def ir_read_signal():
	try:
		write_i2c_block(ir_read_cmd, [unused,unused,unused])
		time.sleep(.1)
		data_back = i2c.read_list(reg = None, len = 22)
		if data_back[1]!=255:
			return data_back
		return [-1]*21
	except IOError:
		return [-1]*21

# Grove - Infrared Receiver- set the pin on which the Grove IR sensor is connected
def ir_recv_pin(pin):
	write_i2c_block(ir_recv_pin_cmd, [pin,unused,unused])

def cpu_speed():
	write_i2c_block(cpu_speed_cmd, [0,0,0])
	time.sleep(.1)
	try:
		b1=i2c.read_8()
		b2=i2c.read_8()
	except IOError:
		return -1
	return b1

# Read the DHT sensor connected to the serial port
def dht(sensor_type=0):
	try:
		import Adafruit_DHT
		if sensor_type==0: #blue sensor
			sensor = Adafruit_DHT.DHT11
		elif sensor_type==1: #white sensor
			sensor = Adafruit_DHT.DHT22
		pin = 15 #connected to the serial port on the GoPiGo, RX pin
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin,retries=3,delay_seconds=.1)
		if humidity is not None and temperature is not None:
			return [temperature,humidity]
		else:
			return [-2.0,-2.0]
	except RuntimeError:
		return [-3.0,-3.0]

def check_version():
	global version
	
	if version == 0:
		for i in range(10):
			raw=analogRead(7)

		if raw>v16_thresh:
			version=16
		else:
			version=14

	return version
