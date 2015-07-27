#!/usr/bin/env python

'''
## License
 GoPiGo for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
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

from gopigo import *
import sys

import atexit
atexit.register(stop)

while True:
	print "\nCmd:",
	a=raw_input()
	if a=='w':
		fwd()
	elif a=='a':
		left()
	elif a=='d':
		right()
	elif a=='s':
		bwd()
	elif a=='x':
		stop()
	elif a=='t':
		increase_speed()
	elif a=='g':
		decrease_speed()
	elif a=='v':
		print volt(),"V"
	elif a=='b': #servo test
		for i in range(180):
			servo(i)
			print i
			time.sleep(.02)
	elif a=='z':
		sys.exit()
	elif a=='u':
		print us_dist(15),'cm'
	elif a=='l':
		led_on(0)
		led_on(1)
		time.sleep(1)
		led_off(0)
		led_off(1)
	elif a=='i':
		motor_fwd()
	elif a=='k':
		motor_bwd()
	elif a=='n':
		left_rot()
	elif a=='m':
		right_rot()
	elif a=='y':
		enc_tgt(1,1,18)
	elif a=='f':
		print "v",fw_ver()
	elif a=='tr':
		val=trim_read()
		if val==-3:
			print "-3, Trim Value Not set"
		else:
			print val-100
	elif a=='tw':
		print "Enter trim value to write to EEPROM(-100 to 100):",
		val=int(raw_input())
		trim_write(val)
		time.sleep(.1)
		print "Value in EEPROM: ",trim_read()-100
	elif a=='tt':
		print "Enter trim value to test(-100 to 100):",
		val=int(raw_input())
		trim_test(val)
		time.sleep(.1)
		print "Value in EEPROM: ",trim_read()-100
	elif a=='st':
		print "Enter Servo position:",
		val=int(raw_input())
		servo(val)
	time.sleep(.1)
