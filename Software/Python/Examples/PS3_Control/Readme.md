Run
sudo apt-get update

Create a folder for the PS3 setup and delete the folder after the installation is complete
(Do all of this in one folder so you can download and delete it when you're done)

sudo apt-get install bluez-utils bluez-compat bluez-hcidump checkinstall libusb-dev  libbluetooth-dev joystick
wget http://www.pabr.org/sixlinux/sixpair.c
gcc -o sixpair sixpair.c -lusb
wget http://sourceforge.net/projects/qtsixa/files/QtSixA%201.5.1/QtSixA-1.5.1-src.tar.gz
tar xfvz QtSixA-1.5.1-src.tar.gz
cd QtSixA-1.5.1/sixad
make
sudo mkdir -p /var/lib/sixad/profiles
sudo checkinstall
sudo update-rc.d sixad defaults
reboot