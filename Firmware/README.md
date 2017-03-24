## Uploading a new firmware to the GoPiGo
First make the update script executable
> sudo chmod + firmware_update.sh

Make sure that the motors are disconnected from the GoPiGo and then run the firmware update:
> sudo ./firmware_update.sh

## Making changes to the GoPiGo Firmware

The GoPiGo uses software servo to control the Servo's so when making changes to the code, do remember to add the **Software Servo library** to the Arduino Libraries folder

Use this tutorial to load the library http://www.dexterindustries.com/Arduberry/how-to-program-the-arduberry/#new_lib .

Press "CTRL+SHIFT+U" to upload the code


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
