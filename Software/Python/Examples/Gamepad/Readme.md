## USB Gamepad Example
### This example controls the GoPiGo using a Logitech F710 Gamepad.

![Logitech Gamepad and the Raspberry Pi Robot](https://raw.githubusercontent.com/DexterInd/GoPiGo/master/Software/Python/Examples/Gamepad/gpg_and_f710.jpg "GoPiGo Raspberry Pi Robot controlled with a Logitech Gamepad")


**Files:**
- gamepad.py : Example of using a usb gamepad to control the GoPiGo
- show_buttons.py : Python script that prints button values as they are pressed on the gamepad


**Overview**
For an in-depth explanation of these script see [this blog post) [http://egoebelbecker.me/2015/06/10/raspberry-pi-and-gamepad-programming-part-2-controlling-the-gopigo/]

The example script uses buttons on the gamepad to control the GoPiGo's movement. The script is written for a Logitech F710, but other gamepads should work. Use the showbuttons script to

**Usage**
- Connect the controller

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
