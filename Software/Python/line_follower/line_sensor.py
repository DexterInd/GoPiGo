#!/usr/bin/env python
# Dexter Industries line sensor python library
#
# This library provides the basic functions to access the sensor data from the line sensor
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# Karan Nayan
# Initial Date: 13 Dec 2015
# Last Updated: 13 Dec 2015
# http://www.dexterindustries.com/
'''
## License
 Copyright (C) 2015  Dexter Industries

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

import smbus
import time
import math
import RPi.GPIO as GPIO
import struct
import operator
import pickle

debug =0

rev = GPIO.RPI_REVISION
if rev == 2 or rev == 3:
	bus = smbus.SMBus(1)
else:
	bus = smbus.SMBus(0)

# I2C Address of Arduino
address = 0x06

# Command Format
# analogRead() command format header
aRead_cmd = [3]
 
# This allows us to be more specific about which commands contain unused bytes
unused = 0

#Add a multipler to each sensor
multp=[-10,-5,0,5,10]

#TRAIN for the first time
#reading when all sensors are at white
# white=[767,815,859,710,700]
white_line=[0]*5
#reading when all sensors are black
# black=[1012,1013,1015,1003,1004]
black_line=[0]*5
#difference between black and white
# range_col=list(map(operator.sub, black, white))
range_col=[0]*5

file_b='black_line.txt'
file_w='white_line.txt'
file_r='range_line.txt'
# Function declarations of the various functions used for encoding and sending
# data from RPi to Arduino

# Write I2C block
def write_i2c_block(address, block):
	try:
		return bus.write_i2c_block_data(address, 1, block)
	except IOError:
		if debug:
			print "IOError"
		return -1
def read_sensor():
	try:
		#if sensor>=0 and sensor <=4:
		bus.write_i2c_block_data(address, 1, aRead_cmd + [unused, unused, unused])
		#time.sleep(.1)
		#bus.read_byte(address)
		number = bus.read_i2c_block_data(address, 1)
		#time.sleep(.05)
		return number[0]* 256 + number[1],number[2]* 256 + number[3],number[4]* 256 + number[5],number[6]* 256 + number[7],number[8]* 256 + number[9]
		
		#return number[0]* 256 + number[1]
		
		time.sleep(.05)
	except IOError:
		return -1,-1,-1,-1,-1
def get_sensorval():
	while True: 
		val=read_sensor()
		print val
		if val[0]<>-1:
			return val
		else:
			#Read once more to clear buffer and remove junk values
			val=read_sensor()

def set_black_line():
	global black_line,white_line,range_col
	for i in range(5):
		val=read_sensor()
	# print val
	if val[0]!=-1:
		black_line=val
	else:
		black_line=[-1]*5
	range_col=list(map(operator.sub, black_line, white_line))
	with open(file_b, 'wb') as f:
		pickle.dump(black_line, f)
	with open(file_r, 'wb') as f:
		pickle.dump(range_col, f)
		
def get_black_line():
	global black_line
	#load default values from files
	try:
		with open(file_b, 'rb') as f:
			black_line = pickle.load(f)
	except Exception, e:
		print "FAIL!"
		print e
		black_line=[0]*5
	return black_line
	
def set_white_line():
	global white_line,black_line,range_col
	for i in range(5):
		val=read_sensor()
	# print val
	if val[0]!=-1:
		white_line=val
	else:
		white_line=[-1]*5
	range_col=list(map(operator.sub, black_line, white_line))
	with open(file_w, 'wb') as f:
		pickle.dump(white_line, f)
	with open(file_r, 'wb') as f:
		pickle.dump(range_col, f)
	
def get_white_line():
	global white_line
	#load default values from files
	try:
		with open(file_w, 'rb') as f:
			white_line = pickle.load(f)
	except:
		white_line=[0]*5
	return white_line
		
def get_range():
	global range_col
	#load default values from files
	try:
		with open(file_r, 'rb') as f:
			range_col = pickle.load(f)
	except:
		range_col=[0]*5
	return range_col
	
def line_position():
	global black_line,white_line,range_col
	#load default values from files
	try:
		with open(file_b, 'rb') as f:
			black_line = pickle.load(f)
	except:
		black_line=[0]*5
		
	try:
		with open(file_w, 'rb') as f:
			white_line = pickle.load(f)
	except:
		white_line=[0]*5
		
	try:
		with open(file_r, 'rb') as f:
			range_col = pickle.load(f)
	except:
		range_col=[0]*5
	
	curr=get_sensorval()
	diff_val=list(map(operator.sub, curr, white_line))
	curr_pos=0
	percent_black_line=[0]*5
	for i in range(5):
		percent_black_line[i]=diff_val[i]*100/range_col[i]
		curr_pos+=percent_black_line[i]*multp[i]
	return curr_pos	
