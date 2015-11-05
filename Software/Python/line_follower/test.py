#!/usr/bin/env python
import line_sensor
import time
from timeit import default_timer as timer
def get_sensorval():
	while True:
		val=line_sensor.read_sensor()
		if val[0]<>-1:
			return val
		#else:
			#Read once more to clear buffer and remove junk values
		#	val=line_sensor.read_sensor()
while True:
	start=timer()
	l0,l1,l2,l3,l4=get_sensorval()
	end=timer()
	print end-start,l0,l1,l2,l3,l4
	#time.sleep(.05)
