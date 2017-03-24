#!/usr/bin/env python
# This program is for testing GoPiGo Hardware.  

'''
## License
 GoPiGo for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
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
from __future__ import print_function
from __future__ import division
from builtins import input
# the above lines are meant for Python3 compatibility.
# they force the use of Python3 functionality for print(), 
# the integer division and input()
# mind your parentheses!

from gopigo import *
import sys

import atexit
atexit.register(stop)

print ("Both motors moving Forward with LED On")
led_on(0)
led_on(1)
fwd()
time.sleep(5)
print ("Both motors stopped with LED Off")
led_off(0)
led_off(1)
stop()
time.sleep(2)
print ("Both motors moving back with LED On")
led_on(0)
led_on(1)
bwd()
time.sleep(5)
print ("Both motors stopped with LED Off")
led_off(0)
led_off(1)
stop()
time.sleep(2)

stop()
stop()