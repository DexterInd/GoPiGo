## PS3 Controller Example
### This example controls the GoPiGo and using a PS3 Dualshock 3 controller

![PS3 Controller and the Raspberry Pi Robot](https://raw.githubusercontent.com/DexterInd/GoPiGo/master/Software/Python/Examples/PS3%20Control/PS3-controller-for-raspberry-pi.jpg "GoPiGo Raspberry Pi Robot controlled with a Playstation3 controller")


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
