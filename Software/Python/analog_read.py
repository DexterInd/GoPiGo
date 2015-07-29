#!/usr/bin/env python
#
# This example is reading from the analog sensors connected to the GoPiGo analog Port A1 like the sound sensor , rotary angle sensor

'''
## License
 GoPiGo for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
 Copyright (C) 2015  Dexter Industries

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


from gopigo import *
while True:
	analog_read_value=analogRead(1)
	# Print non zero values
	if analog_read_value<>0:
		print analog_read_value
	time.sleep(.1)