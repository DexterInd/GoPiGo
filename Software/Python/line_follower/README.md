# GoPiGo Line Follower

This Python library is for the [GoPiGo Line follower](http://www.dexterindustries.com/shop/line-follower-for-gopigo/).

## Files

###Calibration and Utilities
- <strong>line_threshold_set.py:</strong>  Use this program to set the black/white values.  Run once.
- <strong>black_line.txt:</strong>  Holds the black line values.
- <strong>white_line.txt:</strong>  Holds the white line values.
- <strong>range_line.txt:</strong>  Holds the range of values.
- <strong>line_sensor.py:</strong> Library for the line sensor.
- <strong>line_follow.py:</strong> Basic GoPiGo example to use the line sensor.

###Examples
- <strong>basic_example.py:</strong>  This example shows a basic example to read sensor data from the line sensor.
- <strong>check_line_sensor.py:</strong> Checks the I2C bus for the line follower.
- <strong>line_follow.py:</strong>  A very basic example using bang-bang control.
- <strong>line_follow1.py:</strong>  An advanced example of line following using arrays and proportional response.
- <strong>line_position.py:</strong>  This example reads the position of the line the sensor is positioned over.

###Scratch
- <strong>scratch_line.py:</strong>  Runs the sensor in Scratch in the background.
- <strong>line_sensor_gui.py:</strong> The GUI program for calibration.  A visual form of the line_threshold_set.py program.


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
