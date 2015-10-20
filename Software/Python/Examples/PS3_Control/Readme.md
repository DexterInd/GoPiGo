## PS3 Controller Example
### This example controls the GoPiGo and using a PS3 Dualshock 3 controller

![PS3 Controller and the Raspberry Pi Robot](https://raw.githubusercontent.com/DexterInd/GoPiGo/master/Software/Python/Examples/PS3_Control/PS3-controller-for-raspberry-pi.jpg "GoPiGo Raspberry Pi Robot controlled with a Playstation3 controller")


**Files:**
- ps3.py : Python library for getting values from the PS3 controller
- ps3_gpg_example.py :Example for using the PS3 controller with the GoPiGo
- sixpair: used to pair the PS3 controller using bluetooth

**Usage**
- Connect the PS3 controller with the Raspberry Pi using a USB cable and run sixpair

>./sixpair

- Now disconnect the USB cable an press the **PS** button on teh PS3 controller a few times and the run the ps3_gpg_example.py

>python ps3_gpg_example.py

**Note:**
If you are not using Dexter Industries Image, do the following:
- sudo apt-get update
- Create a folder for the PS3 setup and delete the folder after the installation is complete (Do all of this in one folder so you can download and delete it when you're done)
- sudo apt-get install bluez-utils bluez-compat bluez-hcidump checkinstall libusb-dev libbluetooth-dev joystick 
- wget http://www.pabr.org/sixlinux/sixpair.c 
- gcc -o sixpair sixpair.c -lusb 
- wget http://sourceforge.net/projects/qtsixa/files/QtSixA%201.5.1/QtSixA-1.5.1-src.tar.gz 
- tar xfvz QtSixA-1.5.1-src.tar.gz cd QtSixA-1.5.1/sixad 
- make 
- sudo mkdir -p /var/lib/sixad/profiles 
- sudo checkinstall 
- sudo update-rc.d sixad defaults reboot



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
