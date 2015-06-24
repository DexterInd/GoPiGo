#!/usr/bin/env python
#
# This example is reading from the analog sensors connected to the GoPiGo analog Port A1 like the sound sensor , rotary angle sensor
from gopigo import *
while True:
	analog_read_value=analogRead(1)
	# Print non zero values
	if analog_read_value<>0:
		print analog_read_value
	time.sleep(.1)