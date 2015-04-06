#!/usr/bin/env python
from gopigo import *
import sys

import atexit
atexit.register(stop)

while True:
	print "Both motors moving Forward with LED On"
	led_on(0)
	led_on(1)
	fwd()
	time.sleep(5)
	print "Both motors stopped with LED Off"
	led_off(0)
	led_off(1)
	stop()
	time.sleep(2)
	print "Both motors moving back with LED On"
	led_on(0)
	led_on(1)
	bwd()
	time.sleep(5)
	print "Both motors stopped with LED Off"
	led_off(0)
	led_off(1)
	stop()
	time.sleep(2)
	