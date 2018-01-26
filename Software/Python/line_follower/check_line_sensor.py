#!/usr/bin/env python
# Dexter Industries line sensor check script
#
# This program checks the I2C bus for the line follower and also makes a read to make sure that the line sesnor is working properly
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# Karan Nayan
# Initial Date: 13 Dec 2015
# Last Updated: 13 Dec 2015
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
import line_sensor
import time
import subprocess
from timeit import default_timer as timer

debug=0

def get_sensorval():
	while True:
		val=line_sensor.read_sensor()
		if val[0]<>-1:
			return val
		#else:
			#Read once more to clear buffer and remove junk values
		#	val=line_sensor.read_sensor()

def check_line_sensor():
	output = subprocess.check_output(['i2cdetect', '-y','1'])
	if output.find('06') >=0:
		print "--> Line sensor found\n"
		if debug:
			print output
	else:
		print "--> Line sensor not found" 
		print output
		print ""

check_line_sensor()
start=timer()
l0,l1,l2,l3,l4=get_sensorval()
end=timer()
print "Time:\t%.4f s" %(end-start)
print "IR1:\t%d /1023 " %(l0)
print "IR2:\t%d /1023 " %(l1)
print "IR3:\t%d /1023 " %(l2)
print "IR4:\t%d /1023 " %(l3)
print "IR5:\t%d /1023 " %(l4)
