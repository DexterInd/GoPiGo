#!/usr/bin/env python
#
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

import setuptools
setuptools.setup(
	name="ir_receiver",
	description="Drivers and examples for using the ir_receiver in Python with the GoPiGo without LIRC",
	author="Dexter Industries",
	url="http://www.dexterindustries.com/GoPiGo/",
	py_modules=['ir_receiver'],
	#install_requires=open('requirements.txt').readlines(),
)
