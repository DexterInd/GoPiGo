#! /bin/bash
SCRIPT_DIR="$(readlink -f $(dirname $0))"
ROBOT_DIR="${SCRIPT_DIR%/*}"
PIHOME=/home/pi
DEXTERSCRIPT=$PIHOME/Dexter/lib/Dexter/script_tools

source $DEXTERSCRIPT/functions_library.sh

display_welcome_msg() {
  echo " "
	echo "Special thanks to Joe Sanford at Tufts University. This script was derived from his work. Thank you Joe!"
  echo " "
}

install_dependencies() {

    # the sudo apt-get update is already
    # done by the script_tools installer in
    # update_gopigo.sh

    echo " "
    feedback "Installing Dependencies"
    feedback "======================="
    sudo apt-get install git libi2c-dev  i2c-tools minicom libnss-mdns build-essential libffi-dev -y
    sudo apt-get install python-pip python-serial python-rpi.gpio python-smbus python-dev -y
    sudo apt-get install python3-pip python3-serial python3-rpi.gpio python3-smbus python3-dev -y
    sudo pip install -U RPi.GPIO
    sudo pip install pyusb
    sudo pip install numpy
    sudo pip install python-periphery==1.1.0
    sudo pip3 install -U RPi.GPIO
    sudo pip3 install pyusb
    sudo pip3 install numpy
    sudo pip3 install python-periphery==1.1.0

    feedback "Dependencies installed"
}

check_root_user() {
    if [[ $EUID -ne 0 ]]; then
        feedback "FAIL!  This script must be run as such: sudo ./install.sh"
        exit 1
    fi
    echo " "
}

install_wiringpi() {
    # Check if WiringPi Installed

    # using curl piped to bash does not leave a file behind. no need to remove it
    # we can do either the curl - it works just fine
    # sudo curl https://raw.githubusercontent.com/DexterInd/script_tools/master/update_wiringpi.sh | bash
    # or call the version that's already on the SD card
    sudo bash $DEXTERSCRIPT/update_wiringpi.sh
    # done with WiringPi

    # remove wiringPi directory if present
    if [ -d wiringPi ]
    then
        sudo rm -r wiringPi
    fi
    # End check if WiringPi installed
    echo " "
}

install_spi_i2c() {
    feedback "Removing blacklist from /etc/modprobe.d/raspi-blacklist.conf . . ."
    feedback "=================================================================="
    if grep -q "#blacklist i2c-bcm2708" /etc/modprobe.d/raspi-blacklist.conf; then
        echo "I2C already removed from blacklist"
    else
        sudo sed -i -e 's/blacklist i2c-bcm2708/#blacklist i2c-bcm2708/g' /etc/modprobe.d/raspi-blacklist.conf
        echo "I2C removed from blacklist"
    fi
    if grep -q "#blacklist spi-bcm2708" /etc/modprobe.d/raspi-blacklist.conf; then
        echo "SPI already removed from blacklist"
    else
        sudo sed -i -e 's/blacklist spi-bcm2708/#blacklist spi-bcm2708/g' /etc/modprobe.d/raspi-blacklist.conf
        echo "SPI removed from blacklist"
    fi

    #Adding in /etc/modules
    echo " "
    feedback "Adding I2C-dev and SPI-dev in /etc/modules . . ."
    feedback "================================================"
    if grep -q "i2c-dev" /etc/modules; then
        echo "I2C-dev already there"
    else
        echo i2c-dev >> /etc/modules
        echo "I2C-dev added"
    fi
    if grep -q "i2c-bcm2708" /etc/modules; then
        echo "i2c-bcm2708 already there"
    else
        echo i2c-bcm2708 >> /etc/modules
        echo "i2c-bcm2708 added"
    fi
    if grep -q "spi-dev" /etc/modules; then
        echo "spi-dev already there"
    else
        echo spi-dev >> /etc/modules
        echo "spi-dev added"
    fi
    echo " "
    feedback "Making I2C changes in /boot/config.txt . . ."
    feedback "================================================"

    sudo sh -c "echo dtparam=i2c1=on >> /boot/config.txt"
    sudo sh -c "echo dtparam=i2c_arm=on >> /boot/config.txt"

    sudo adduser pi i2c
    echo " "
}

install_control_panel() {
    sudo cp "$ROBOT_DIR/Software/Python/control_panel/gopigo_control_panel.desktop" $PIHOME/Desktop
}

############################################################################
############################################################################

check_root_user
install_dependencies
# copy software servo
sudo cp -R $ROBOT_DIR/Firmware/SoftwareServo/ /usr/share/arduino/libraries/
# copy gopigo executable
# the gopigo executable is for reporting data about the gopigo board
sudo chmod +x gopigo
sudo cp gopigo /usr/bin
install_DHT
install_wiringpi
install_spi_i2c
install_control_panel

sudo chmod +x $ROBOT_DIR/Software/Scratch/GoPiGo_Scratch_Scripts/*.sh
