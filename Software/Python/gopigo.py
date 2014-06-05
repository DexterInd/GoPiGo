#!/usr/bin/python
import serial, time
import smbus
import math
import RPi.GPIO as GPIO
import struct

import smbus
import time

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x08

fwd_cmd=[119]
bwd_cmd=[115]
left_cmd=[97]
right_cmd=[100]
stop_cmd=[120]
ispd_cmd=[116]
dspd_cmd=[103]
volt_cmd=[118]
us_cmd=[117]
led_cmd=[108]

LED_L=1
LED_R=0
#Write I2C block
def write_i2c_block(address,block):
	try:
		return bus.write_i2c_block_data(address,1,block)
	except IOError:
		print "IOError"
		return -1
		
def writeNumber(value):
    bus.write_byte(address, value)
    # bus.write_byte_data(address, 0, value) 
    return -1

def readNumber():
    number = bus.read_byte(address)
    # number = bus.read_byte_data(address, 1)
    return number

#time.sleep(1)
#i=0
#while True:
	#a=raw_input()
	#print ord(a)
	#writeNumber(ord(a))
	#time.sleep(.1)

def fwd():
	return write_i2c_block(address,fwd_cmd+[0,0,0])
def bwd():
	return write_i2c_block(address,bwd_cmd+[0,0,0])
def left():
	return write_i2c_block(address,left_cmd+[0,0,0])
def right():
	return write_i2c_block(address,right_cmd+[0,0,0])
def stop():
	return write_i2c_block(address,stop_cmd+[0,0,0])
def increase_speed():
	return write_i2c_block(address,ispd_cmd+[0,0,0])
def decrease_speed():
	return write_i2c_block(address,dspd_cmd+[0,0,0])
def volt():
	bus.write_i2c_block_data(address,1,volt_cmd+[0,0,0])
	time.sleep(.1)
	#bus.read_byte(address)
	number = bus.read_i2c_block_data(address,1)
	v=number[0]*256+number[1]
	v=(5*float(v)/1024)/.4
	return v
def us_dist(pin):
	write_i2c_block(address,us_cmd+[pin,0,0])
	time.sleep(.1)
	#bus.read_byte(address)
	number = bus.read_i2c_block_data(address,1)
	dist=number[0]*256+number[1]
	return dist
def led(l_id,power):
	if l_id==LED_L or l_id==LED_R:
		write_i2c_block(address,led_cmd+[l_id,power,0])
		return 1
	else:
		return -1
def led_on(l_id):
	if l_id==LED_L or l_id==LED_R:
		write_i2c_block(address,led_cmd+[l_id,255,0])
		return 1
	else:
		return -1
def led_off(l_id):
	if l_id==LED_L or l_id==LED_R:
		write_i2c_block(address,led_cmd+[l_id,0,0])
		return 1
	else:
		return -1
'''
ser = serial.Serial('/dev/ttyAMA0',  9600, timeout = 0)
def fwd():
	send('w')
def bwd():
	send('s')
def left():
	send('a')
def right():
	send('d')
def stop():
	send('x')
def increase_speed():
	send('t')
def decrease_speed():
	send('g')
def volt():
	send('v')
	try:
		volt=ser.readline()
	except ser.SerialTimeoutException:
		print('Data could not be read')
	volt=int(volt)
	volt=(5*float(volt)/1024)/.4
	return volt
def us_dist(pin):
	send('u'+chr(pin))
	
	try:
		volt=ser.readline()
	except ser.SerialTimeoutException:
		print('Data could not be read')
	#volt=int(volt)
	return volt

def servo(position):
	send('b'+chr(position))
	
#if you only want to send data to arduino
def send( theinput ):
  ser.write( theinput )
  while True:
    try:
      time.sleep(0.01)
      break
    except:
      pass
  time.sleep(0.1)

#if you would like to tell the arduino that you would like to receive data from the arduino
def send_and_receive( theinput ):
  ser.write( theinput )
  while True:
    try:
      time.sleep(0.01)
      state = ser.readline()
      return state
    except:
      pass
  time.sleep(0.1)
  '''