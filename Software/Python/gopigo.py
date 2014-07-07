#!/usr/bin/python
########################################################################                                                                  
# This library is for communicating with the GoPiGo                                
# http://www.dexterindustries.com/GoPiGo/                                                                
# History
# ------------------------------------------------
# Author     Date      		Comments
# Karan      30 March 14  	Initial Authoring
# 			 02 July  14	Removed bugs and some features added (v0.9)                                                              
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)           
#
########################################################################
import serial, time
import smbus
import math
import RPi.GPIO as GPIO
import struct

import smbus
import time
import subprocess
# for RPI version 1, use "bus = smbus.SMBus(0)"
rev = GPIO.RPI_REVISION
if rev == 2:
	bus = smbus.SMBus(1) 
else:
	bus = smbus.SMBus(0) 

# This is the address for the GoPiGo
address = 0x08

#GoPiGo Commands
fwd_cmd				=[119]
motor_fwd_cmd		=[105]
bwd_cmd				=[115]
motor_bwd_cmd		=[107]
left_cmd			=[97]
left_rot_cmd		=[98]
right_cmd			=[100]
right_rot_cmd		=[110]
stop_cmd			=[120]
ispd_cmd			=[116]
dspd_cmd			=[103]
volt_cmd			=[118]
us_cmd				=[117]
led_cmd				=[108]
servo_cmd			=[101]
enc_tgt_cmd			=[50]
fw_ver_cmd			=[20]
en_enc_cmd			=[51]
dis_enc_cmd			=[52]
en_servo_cmd		=[61]
dis_servo_cmd		=[60]
set_left_speed_cmd	=[70]
set_right_speed_cmd	=[71]
en_com_timeout_cmd	=[80]
dis_com_timeout_cmd	=[81]

LED_L=1
LED_R=0

#Enable slow i2c
def en_slow_i2c():
	#subprocess.call('sudo rmmod i2c_bcm2708',shell=True)
	subprocess.call('sudo modprobe i2c_bcm2708 baudrate=70000',shell=True)
	
#Write I2C block
def write_i2c_block(address,block):
	try:
		return bus.write_i2c_block_data(address,1,block)
	except IOError:
		print "IOError"
		return -1
	return 1

#Write a byte 
def writeNumber(value):
	try:
		bus.write_byte(address, value)
	except IOError:
		print "IOError"
		return -1	
	return 1

#Read a byte
def readByte():
	try:
		number = bus.read_byte(address)
	except IOError:
		print "IOError"
		return -1	
	return number

#Move the GoPiGo forward
def fwd():
	return write_i2c_block(address,fwd_cmd+[0,0,0])
	
#Move the GoPiGo forward without PID
def motor_fwd():
	return write_i2c_block(address,motor_fwd_cmd+[0,0,0])

#Move GoPiGo backward
def bwd():
	return write_i2c_block(address,bwd_cmd+[0,0,0])

#Move GoPiGo backward without PID control
def motor_bwd():
	return write_i2c_block(address,motor_bwd_cmd+[0,0,0])

#Turn GoPiGo Left slow (one motor off, better control)	
def left():
	return write_i2c_block(address,left_cmd+[0,0,0])

#Rotate GoPiGo left in same position
def left_rot():
	return write_i2c_block(address,left_rot_cmd+[0,0,0])

#Turn GoPiGo right slow (one motor off, better control)
def right():
	return write_i2c_block(address,right_cmd+[0,0,0])

#Rotate GoPiGo right in same position
def right_rot():
	return write_i2c_block(address,right_rot_cmd+[0,0,0])

#Stop the GoPiGo
def stop():
	return write_i2c_block(address,stop_cmd+[0,0,0])
	
#Increase the speed
def increase_speed():
	return write_i2c_block(address,ispd_cmd+[0,0,0])
	
#Decrease the speed
def decrease_speed():
	return write_i2c_block(address,dspd_cmd+[0,0,0])

#Read voltage
#	return:	voltage in V
def volt():
	write_i2c_block(address,volt_cmd+[0,0,0])
	time.sleep(.1)
	try:
		b1=bus.read_byte(address)
		b2=bus.read_byte(address)
	except IOError:
		return -1
	
	if b1!=-1 and b2!=-1:
		v=b1*256+b2
		v=(5*float(v)/1024)/.4
		return round(v,2)
	else:
		return -1
#Read ultrasonic sensor
#	arg:
#		pin -> 	Pin number on which the US sensor is connected
#	return:		distance in cm
def us_dist(pin):
	write_i2c_block(address,us_cmd+[pin,0,0])
	time.sleep(.08)
	try:
		b1=bus.read_byte(address)
		b2=bus.read_byte(address)
	except IOError:
		return -1
	if b1!=-1 and b2!=-1:
		v=b1*256+b2
		return v
	else:
		return -1

#Set led to the power level 
#	arg:
#		l_id:	1 for left LED and 0 for right LED
#		power:	pwm power for the LED's
def led(l_id,power):
	if l_id==LED_L or l_id==LED_R:
		write_i2c_block(address,led_cmd+[l_id,power,0])
		return 1
	else:
		return -1

#Turn led on
#	arg:
#		l_id: 1 for left LED and 0 for right LED
def led_on(l_id):
	if l_id==LED_L or l_id==LED_R:
		write_i2c_block(address,led_cmd+[l_id,255,0])
		return 1
	else:
		return -1

#Turn led off
#	arg:
#		l_id: 1 for left LED and 0 for right LED
def led_off(l_id):
	if l_id==LED_L or l_id==LED_R:
		write_i2c_block(address,led_cmd+[l_id,0,0])
		return 1
	else:
		return -1
		
#Set servo position
#	arg:
#		position: angle in degrees to set the servo at
def servo(position):
	write_i2c_block(address,servo_cmd+[position,0,0])
	
#Set encoder targeting on
#arg:
#	m1: 0 to disable targeting for m1, 1 to enable it
#	m2:	1 to disable targeting for m2, 1 to enable it
#	target: number of encoder pulses to target (18 per revolution)
def enc_tgt(m1,m2,target):
	if m1>1 or m1<0 or m2>1 or m2<0:
		return -1
	m_sel=m1*2+m2
	write_i2c_block(address,enc_tgt_cmd+[m_sel,target/256,target%256])
	return 1
	
#Read status
#	return:	0 if encoder target is reached
def read_status():
	st=bus.read_byte(address)
	return st
	
#Returns the firmware version
def fw_ver():
	write_i2c_block(address,fw_ver_cmd+[0,0,0])
	time.sleep(.1)
	try:
		ver=bus.read_byte(address)
		bus.read_byte(address)		#Empty the buffer
	except IOError:
		return -1
	return float(ver)/10

#Enable the encoders (enabled by default)
def enable_encoders():
	return write_i2c_block(address,en_enc_cmd+[0,0,0])
	
#Disable the encoders (use this if you don't want to use the encoders)
def disable_encoders():
	return write_i2c_block(address,dis_enc_cmd+[0,0,0])
	
#Enables the servo
def enable_servo():
	return write_i2c_block(address,en_servo_cmd+[0,0,0])

#Disable the servo
def disable_servo():
	return write_i2c_block(address,dis_servo_cmd+[0,0,0])

#Set speed of the left motor
#	arg:
#		speed-> 0-255
def set_left_speed(speed):
	if speed >255:
		speed =255
	elif speed <0:
		speed =0
	return write_i2c_block(address,set_left_speed_cmd+[speed,0,0])
	
#Set speed of the right motor
#	arg:
#		speed-> 0-255
def set_right_speed(speed):
	if speed >255:
		speed =255
	elif speed <0:
		speed =0
	return write_i2c_block(address,set_right_speed_cmd+[speed,0,0])

#Set speed of the both motors
#	arg:
#		speed-> 0-255
def set_speed(speed):
	if speed >255:
		speed =255
	elif speed <0:
		speed =0
	set_left_speed(speed)
	time.sleep(.1)
	set_right_speed(speed)

def enable_com_timeout(timeout):
	return write_i2c_block(address,en_com_timeout_cmd+[timeout/256,timeout%256,0])
	
def disable_com_timeout():
	return write_i2c_block(address,dis_com_timeout_cmd+[0,0,0])