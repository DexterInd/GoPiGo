#! /usr/bin/env python
from gopigo import *

print "---------------------------\n|",
ver=fw_ver()

if ver==-1:
	print "| GoPiGo Not Found"
	print "---------------------------"
	exit()

print "GoPiGo Found"
print "| Firmware version:",ver
print "| Battery voltage :",volt(),"V"
print "---------------------------"
