## USB Gamepad Example
### This example controls the GoPiGo using a Logitech F710 Gamepad.

![Logitech Gamepad and the Raspberry Pi Robot](https://raw.githubusercontent.com/egoebelbecker/GoPiGo/master/Software/Python/Examples/Gamepad/gpg_and_f710.jpg "GoPiGo Raspberry Pi Robot controlled with a Logitech Gamepad")


**Files:**
- gamepad.py : Example of using a usb gamepad to control the GoPiGo
- show_buttons.py : Python script that prints button values as they are pressed on the gamepad


**Overview:**

For an in-depth explanation of these script see [this blog post] (http://egoebelbecker.me/2015/06/10/raspberry-pi-and-gamepad-programming-part-2-controlling-the-gopigo/)

The example script uses buttons on the gamepad to control the GoPiGo's movement. The script is written for a Logitech F710, but other gamepads should work. Use the showbuttons script to display the button values on your gamepad and modify the script.

**Usage**
- Connect the controller.
- Open a terminal session via vnc or ssh.
- Make sure gamepad.py is executable:   chmod +x gamepad.py
- Run gamepad.py.
- The script will print the direction you specify via the gamepad, as well as move the GoPiGo.
- For the Logitech gamepad A-B-X-Y control direction.
- Clicking on the right hand joystick stops the GoPiGo.
- LB and RB on the front of the Gamepad control speed.
- See the script comments for how to modify for different controllers.



![ GoPiGo ](https://raw.githubusercontent.com/DexterInd/GoPiGo/master/GoPiGo_Chassis-300.jpg)

This repository contains source code, firmware and design materials for the GoPiGo.

![ GoPiGo ](https://raw.githubusercontent.com/DexterInd/GoPiGo/master/GoPiGo_Front_Facing_Camera300.jpg)

# See Also

- [Dexter Industries] (http://www.dexterindustries.com/GoPiGo)
- [Kickstarter Campaign] (http://kck.st/Q6vVOP)
- [Raspberry Pi] (http://www.raspberrypi.org/)


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
