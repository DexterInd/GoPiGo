#!/usr/bin/env python
# This example is to control the LED's connected to the analog and digital ports of the GoPiGo

from gopigo import *
import time

#Pin number for the grove analog port A0
analog_pin=15

#Pin number for the grove digital port D11
digital_pin=10

#Setting the port to output
pinMode(analog_pin,"OUTPUT")
pinMode(digital_pin,"OUTPUT")
while True:
	print "ON"
	digitalWrite(analog_pin,1)
	digitalWrite(digital_pin,1)
	time.sleep(.5)
	
	print "OFF"
	digitalWrite(analog_pin,0)
	digitalWrite(digital_pin,0)
	time.sleep(.5)
