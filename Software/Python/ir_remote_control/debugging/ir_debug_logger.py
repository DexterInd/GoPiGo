#!/usr/bin/env python
from subprocess import Popen, PIPE, STDOUT, call
import datetime
import time

# Before running this program, please make sure [ir-server.service] is stopped
# After the program has finished, please turn [ir-server.service] back on 

call("sudo /etc/init.d/lirc stop", shell=True)
time.sleep(.5)

p = Popen('mode2 -d /dev/lirc0', stdout = PIPE, stderr = STDOUT, shell = True)
print "Logging started, Press Ctrl+C to stop"
f=open("/home/pi/Desktop/ir_raw_sig_log.txt","a")
f.write(str(datetime.datetime.now()))
f.close()

while True:
    # Read the raw value from the IR receiver

    line = p.stdout.readline()
    if len(line)!=0:
        f=open("/home/pi/Desktop/ir_raw_sig_log.txt","a")
        f.write(line)
        f.close()
        print line,
