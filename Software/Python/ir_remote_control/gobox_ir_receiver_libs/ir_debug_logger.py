#!/usr/bin/env python 
from subprocess import Popen, PIPE, STDOUT, call
import datetime
import time

call("sudo /etc/init.d/lirc stop", shell=True)
time.sleep(.5)

# Stop the DI ir reader running in the background to enable the debug logging 
p = Popen('sudo monit stop di_ir_reader', stdout = PIPE, stderr = STDOUT, shell = True) 

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
