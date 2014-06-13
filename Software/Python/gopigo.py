#!/usr/bin/python
import serial, time
import smbus
import math
import RPi.GPIO as GPIO
import struct

import smbus
import time

# for RPI version 1, use "bus = smbus.SMBus(0)"
rev = GPIO.RPI_REVISION
if rev == 2:
	bus = smbus.SMBus(1) 
else:
	bus = smbus.SMBus(0) 

# This is the address we setup in the Arduino Program
address = 0x08

#GoPiGo Commands
fwd_cmd=[119]
motor_fwd_cmd=[105]
bwd_cmd=[115]
motor_bwd_cmd=[107]
left_cmd=[97]
left_rot_cmd=[98]
right_cmd=[100]
right_rot_cmd=[110]
stop_cmd=[120]
ispd_cmd=[116]
dspd_cmd=[103]
volt_cmd=[118]
us_cmd=[117]
led_cmd=[108]
servo_cmd=[101]
enc_tgt_cmd=[50]
LED_L=1
LED_R=0

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
def volt():
	write_i2c_block(address,volt_cmd+[0,0,0])
	time.sleep(.1)
	try:
		b1=bus.read_byte(address)
		b2=bus.read_byte(address)
	except IOError:
		return -1
	print b1,b2
	if b1!=-1 and b2!=-1:
		v=b1*256+b2
		v=(5*float(v)/1024)/.4
		return v
	else:
		return -1
#Read ultrasonic sensor
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
def led(l_id,power):
	if l_id==LED_L or l_id==LED_R:
		write_i2c_block(address,led_cmd+[l_id,power,0])
		return 1
	else:
		return -1

#Turn led on
def led_on(l_id):
	if l_id==LED_L or l_id==LED_R:
		write_i2c_block(address,led_cmd+[l_id,255,0])
		return 1
	else:
		return -1

#Turn led off
def led_off(l_id):
	if l_id==LED_L or l_id==LED_R:
		write_i2c_block(address,led_cmd+[l_id,0,0])
		return 1
	else:
		return -1
		
#Set servo postion
def servo(position):
	write_i2c_block(address,servo_cmd+[position,0,0])
	
#Set encoder targetting on
def enc_tgt(m1,m2,target):
	if m1>1 or m1<0 or m2>1 or m2<0:
		return -1
	m_sel=m1*2+m2
	write_i2c_block(address,enc_tgt_cmd+[m_sel,target/256,target%256])
	return 1
	
#Read status
def read_status():
	st=bus.read_byte(address)
	return st