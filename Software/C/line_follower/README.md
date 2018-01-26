# GoPiGo Line Follower

This C library is for the [GoPiGo Line follower](http://www.dexterindustries.com/shop/line-follower-for-gopigo/).

#####To Compile:  gcc line_sensor.c [your_file_name.c] -o gopigo -Wall
#####To run: ./gopigo

**Notes:**
- The compile command uses the basic commands from line_sensor.c library 
- The output exectuable is the one followed by the -o argument, which is gopigo here (You can change it to something else if yuo want)
- the -Wall argument enable's all compiler warnings and is necessary for compiling the GoPiGo C example. Read more about it here: http://www.rapidtables.com/code/linux/gcc/gcc-wall.htm

## Files

###Calibration and Utilities
- <strong>line_sensor.c:</strong>  Library for the line sensor.
- <strong>line_sensor.h</strong>  Header file of the line sensor library.

###Examples
- <strong>sensor_read.c:</strong>  This example shows a basic example to read sensor data from the line sensor.


## See Also

- [Dexter Industries] (http://www.dexterindustries.com/GoPiGo)
- [Raspberry Pi] (http://www.raspberrypi.org/)

![ GoPiGo ](https://raw.githubusercontent.com/DexterInd/GoPiGo/master/GoPiGo_Chassis-300.jpg)

This repository contains source code, firmware and design materials for the GoPiGo.

![ GoPiGo ](https://raw.githubusercontent.com/DexterInd/GoPiGo/master/GoPiGo_Front_Facing_Camera300.jpg)

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
