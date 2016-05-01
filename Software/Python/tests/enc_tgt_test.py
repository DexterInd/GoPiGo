#!/usr/bin/env python
from gopigo import *
import sys

import atexit
atexit.register(stop)

enable_encoders()

print "\nCHECKING ENCODER READINGS"
print enc_read(0),
print enc_read(1)
print "Both motors moving Forward with LED On"
led_on(0)
led_on(1)
fwd()
time.sleep(5)
print "after 5 sec",
print enc_read(0),
print enc_read(1)
print "Both motors stopped with LED Off"
led_off(0)
led_off(1)
ret = stop()
print ret,
print "after stop cmd",
print enc_read(0),
print enc_read(1)
time.sleep(2)
print ret,
print "after 2 more sec",
print enc_read(0),
print enc_read(1)
print "Both motors moving back with LED On"
led_on(0)
led_on(1)
bwd()
time.sleep(5)
print "after 5 sec",
print enc_read(0),
print enc_read(1)
print "Both motors stopped with LED Off"
led_off(0)
led_off(1)
ret = stop()
print ret,
print "after stop cmd",
print enc_read(0),
print enc_read(1)
time.sleep(2)
print ret,
print "after 2 more sec ",
print enc_read(0),
print enc_read(1)
	
print "\nCHECKING ENCODER TARGETING"
for i in range(5):
	j=0
	print "\nInitial encoder read vals:",
	fwd()
	enc_tgt(1,1,72)
	print enc_read(0),
	print enc_read(1)
	while True:
		if j>10:
			print "FAIL"
			break
		j+=1
		enc_stat=read_enc_status()
		print "Enc tgt Status: ",enc_stat
		if enc_stat==0:
			break;
		time.sleep(.5)
	print "Final encoder read vals:",
	print enc_read(0),
	print enc_read(1)
	time.sleep(1)