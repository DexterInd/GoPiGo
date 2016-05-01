## Office Cannon
### This example controls the GoPiGo and Office Cannon with a wireless mouse on the USB port.

![A Mobile Office cannon with the Raspberry Pi robot](https://raw.githubusercontent.com/DexterInd/GoPiGo/master/Software/Python/Examples/Office_Cannon/Office-cannon-with-raspberry-pi.jpg "Office cannon with the Raspberry Pi robot")

**Control:**

- Move the mouse up, down, left or right to control the cannon
- Press any mouse button to start moving the GoPiGo.
- Press Left mouse button to turn the GoPiGo left
- Press Right mouse button to turn the GoPiGo right
- Press both the left and right mouse buttons to stop
- Press the middle mouse button to fire

**Note:**

- The office cannon needs more than the 600mA that is supplied by USB to fire the projectiles.
- For this, the we pull the GPIO 32 to HIGH which allows the USB to supply upto 1.2A.
- The USB power supply is reverted back to normal when the program closes or when the user uses CTRL+CTRL to close the program.




![ GoPiGo ](https://raw.githubusercontent.com/DexterInd/GoPiGo/master/GoPiGo_Chassis-300.jpg)

This repository contains source code, firmware and design materials for the GoPiGo.

![ GoPiGo ](https://raw.githubusercontent.com/DexterInd/GoPiGo/master/GoPiGo_Front_Facing_Camera300.jpg)

# See Also

- [Dexter Industries] (http://www.dexterindustries.com/GoPiGo)
- [Kickstarter Campaign] (http://kck.st/Q6vVOP)
- [Raspberry Pi] (http://www.raspberrypi.org/)


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
