#! /bin/bash
SCRIPT_DIR="$(readlink -f $(dirname $0))"
ROBOT_DIR="${SCRIPT_DIR%/*}"
PIHOME=/home/pi
DEXTERSCRIPT=$PIHOME/Dexter/lib/Dexter/script_tools

source $DEXTERSCRIPT/functions_library.sh

display_welcome_msg() {
	echo "Special thanks to Joe Sanford at Tufts University. This script was derived from his work. Thank you Joe!"
}

install_dependencies() {

    # the sudo apt-get update is already
    # done by the script_tools installer in
    # update_gopigo.sh

    feedback "Installing dependencies for the GoPiGo"
    sudo apt-get install --no-install-recommends -y \
        git libi2c-dev i2c-tools libnss-mdns build-essential libffi-dev \
        python-pip python-serial python-rpi.gpio python-smbus python-dev \
        python3-pip python3-serial python3-rpi.gpio python3-smbus python3-dev

    feedback "Dependencies installed for the GoPiGo"
}

check_root_user() {
    if [[ $EUID -ne 0 ]]; then
        feedback "FAIL!  This script must be run as such: sudo ./install.sh"
        exit 1
    fi
}

install_spi_i2c() {
    feedback "Removing blacklist from /etc/modprobe.d/raspi-blacklist.conf . . ."
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
    feedback "Adding I2C-dev and SPI-dev in /etc/modules . . ."
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
    feedback "Making I2C changes in /boot/config.txt . . ."

    sudo sh -c "echo dtparam=i2c1=on >> /boot/config.txt"
    sudo sh -c "echo dtparam=i2c_arm=on >> /boot/config.txt"

    sudo adduser pi i2c
}

install_avr() {
  feedback "Installing avrdude for the GoPiGo"
	source $DEXTERSCRIPT/install_avrdude.sh
  create_avrdude_folder
  install_avrdude
  cd $ROBOT_DIR
  echo "done with AVRDUDE "
}

install_control_panel() {
    cp "$ROBOT_DIR/Software/Python/control_panel/gopigo_control_panel.desktop" $PIHOME/Desktop
}

############################################################################
############################################################################

check_root_user
install_dependencies

# copy software servo
# we might also want to delete $ROBOT_DIR/Firmware/SoftwareServo from the repo for good
# sudo cp -R $ROBOT_DIR/Firmware/SoftwareServo/ /usr/share/arduino/libraries/

# copy gopigo executable
# the gopigo executable is for reporting data about the gopigo board
sudo chmod +x gopigo
sudo cp gopigo /usr/bin
install_spi_i2c
install_avr
install_control_panel

sudo chmod +x $ROBOT_DIR/Software/Scratch/GoPiGo_Scratch_Scripts/*.sh
