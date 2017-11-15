#!/usr/bin/env python
# Dexter Industries line sensor python library
#
# This library provides the basic functions to access the sensor data from the line sensor
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# Karan Nayan
# Initial Date: 13 Dec 2015
# Last Updated: 05 Apr 2017
# http://www.dexterindustries.com/
'''
## License
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
from __future__ import print_function
#from __future__ import division
from builtins import input
# the above lines are meant for Python3 compatibility.
# they force the use of Python3 functionality for print(),
# the integer division and input()
# mind your parentheses!

import time
import math
import RPi.GPIO as GPIO
import struct
import operator
import pickle
import numpy

from periphery import I2C, I2CError
# We are using [python-periphery] package because with the
# latest kernel versions (>v4.4.50-v7) and with the [python-smbus] package
# the line follower no longer works. The issue is with the line follower,
# which doesn't know how to process repeated starts from the master.
# With [python-periphery] package, it's possible to avoid issuing
# repeated start conditions and instead just use start/stop conditions.
# original report: https://github.com/raspberrypi/firmware/issues/828
# dev issue      : https://github.com/RobertLucian/GoPiGo/issues/8
# PR             : https://github.com/DexterInd/GoPiGo/pull/273


debug = 0

rev = GPIO.RPI_REVISION
if rev == 2 or rev == 3:
	bus_number = 1
else:
	bus_number = 0

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

dir_path="/home/pi/Dexter/"
file_b=dir_path+'black_line.txt'
file_w=dir_path+'white_line.txt'
file_r=dir_path+'range_line.txt'
# Function declarations of the various functions used for encoding and sending
# data from RPi to Arduino

# buffer with raw data from the line follower sensor
sensor_buffer = [ [], [], [], [], [] ]
# keep a maximum of 20 readings for each IR sensor on the line follower
max_buffer_length = 20

# Function for removing outlier values
# For bigger std_factor_threshold, the filtering is less aggressive
# For smaller std_factor_threshold, the filtering is more aggressive
# std_factor_threshold must be bigger than 0
def statisticalNoiseReduction(values, std_factor_threshold = 2):
    if len(values) == 0:
    	return []

    mean = numpy.mean(values)
    standard_deviation = numpy.std(values)

    # just return if we only got constant values
    if standard_deviation == 0:
    	return values

    # remove outlier values which are less than the average but bigger than the calculated threshold
    filtered_values = [element for element in values if element > mean - std_factor_threshold * standard_deviation]
    # the same but in the opposite direction
    filtered_values = [element for element in filtered_values if element < mean + std_factor_threshold * standard_deviation]

    return filtered_values

# Function for reading line follower's values off of its IR sensor
def read_sensor():
    address = 0x06
    register = 0x01
    command = 0x03
    unused = 0x00

    try:
        i2c = I2C('/dev/i2c-' + str(bus_number))

        read_bytes = 10 * [0]
        msg1 = [ I2C.Message([register, command] + 3 * [unused]) ]
        msg2 = [ I2C.Message(read_bytes, read=True) ]
        # we meed to do 2 transfers so we can avoid using repeated starts
        # repeated starts don't go hand in hand with the line follower
        i2c.transfer(address, msg1)
        i2c.transfer(address, msg2)
        
    except I2CError as error:
        return 5 * [-1]

    # unpack bytes received and process them
    # bytes_list = struct.unpack('10B',read_results[0])
    output_values = []
    input_values = msg2[0].data

    for step in range(5):
        # calculate the 16-bit number we got
        sensor_buffer[step].append(input_values[2 * step] * 256 + input_values[2 * step + 1])

        # if there're too many elements in the list
        # then remove one
        if len(sensor_buffer[step]) > max_buffer_length:
            sensor_buffer[step].pop(0)

        # eliminate outlier values and select the most recent one
        filtered_value = statisticalNoiseReduction(sensor_buffer[step], 2)[-1]

        # append the value to the corresponding IR sensor
        output_values.append(filtered_value)

    return output_values

def get_sensorval():

	# updated to avoid an infinite loop
	attempt = 0
	while attempt < 5:
		val=read_sensor()
		# print (val)
		if val[0]!=-1:
			return val
		else:
			#Read once more to clear buffer and remove junk values
			val=read_sensor()
			attempt = attempt + 1

	return val


def set_black_line():
	global black_line, white_line, range_col
	for i in range(5):
		val=read_sensor()
	# print (val)
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
	except Exception as e:
		print ("Line Follower: failed getting black line values!")
		print (e)
		black_line=[0]*5
	return black_line


def set_white_line():
	global white_line,black_line,range_col
	for i in range(5):
		val=read_sensor()
	# print (val)
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
		# casting to int when moving to Python 3
		percent_black_line[i]=(diff_val[i]*100/range_col[i])
		curr_pos+=percent_black_line[i]*multp[i]
	return curr_pos
