#! /bin/bash

called_from_di_update() {
    if [[ -f /home/pi/quiet_mode ]]
    then
        quiet_mode=1
        return 1
    else
        quiet_mode=0
        return 0
    fi
}
not_called_from_di_update() {
    if called_from_di_update; then
        return 0
    else
        return 1
    fi
}

identify_cie() {
    if not_called_from_di_update
    then
        echo "  _____            _                                ";
        echo " |  __ \          | |                               ";
        echo " | |  | | _____  _| |_ ___ _ __                     ";
        echo " | |  | |/ _ \ \/ / __/ _ \ '__|                    ";
        echo " | |__| |  __/>  <| ||  __/ |                       ";
        echo " |_____/ \___/_/\_\\\__\___|_|          _            ";
        echo " |_   _|         | |         | |      (_)           ";
        echo "   | |  _ __   __| |_   _ ___| |_ _ __ _  ___  ___  ";
        echo "   | | | '_ \ / _\ | | | / __| __| '__| |/ _ \/ __| ";
        echo "  _| |_| | | | (_| | |_| \__ \ |_| |  | |  __/\__ \ ";
        echo " |_____|_| |_|\__,_|\__,_|___/\__|_|  |_|\___||___/ ";
        echo "                                                    ";
        echo "                                                    ";
        echo " "
    fi
}

identify_robot() {
echo "  ______  _____   _____  _____  ______  _____ "
echo " |  ____ |     | |_____]   |   |  ____ |     |"
echo " |_____| |_____| |       __|__ |_____| |_____|"
echo " "
echo "Welcome to GoPiGo Installer." 
echo " "
}

check_root_user() {
    if [[ $EUID -ne 0 ]]; then
        echo "FAIL!  This script must be run as such: sudo ./install.sh"
        exit 1
    fi
    echo " "
}

check_internet() {
    if not_called_from_di_update; then
        echo "Check for internet connectivity..."
        echo "=================================="
        wget -q --tries=2 --timeout=20 --output-document=/dev/null http://raspberrypi.org 
        if [ $? -eq 0 ];then
            echo "Connected to the Internet"
        else
            echo "Unable to Connect, try again !!!"
            exit 0
        fi
    fi
}



display_welcome_msg() {
    echo "Please ensure internet connectivity before running this script."
    if not_called_from_di_update
    then
        echo "NOTE: Raspberry Pi will need to be rebooted after completion."
    fi

    echo "Special thanks to Joe Sanford at Tufts University.  This script was derived from his work.  Thank you Joe!"
    echo " "
}

install_dependencies() {
    if not_called_from_di_update; then
        sudo apt-get update
    fi
    echo " "
    echo "Installing Dependencies"
    echo "======================="
    sudo apt-get install python-pip git libi2c-dev python-serial python-rpi.gpio i2c-tools python-smbus arduino minicom libnss-mdns python-dev -y
    sudo pip install -U RPi.GPIO

    echo "Dependencies installed"
}

install_DHT() {
    # Install the DHT library
    echo "Installing DHT library"
    pushd $ROBOT_DIR/Software/Python/sensor_examples/dht/Adafruit_Python_DHT
    sudo python setup.py install
    sudo python3 setup.py install
    popd $ROBOT_DIR/Setup/
}

install_wiringpi() {
    # Check if WiringPi Installed
    # Check if WiringPi Installed and has the latest version.  If it does, skip the step.
    version=`gpio -v`       # Gets the version of wiringPi installed
    set -- $version         # Parses the version to get the number
    WIRINGVERSIONDEC=$3     # Gets the third word parsed out of the first line of gpio -v returned.
                                            # Should be 2.36
    echo $WIRINGVERSIONDEC >> tmpversion    # Store to temp file
    VERSION=$(sed 's/\.//g' tmpversion)     # Remove decimals
    rm tmpversion                           # Remove the temp file

    echo "VERSION is $VERSION"
    if [ $VERSION -eq '236' ]; then

        echo "FOUND WiringPi Version 2.36 No installation needed."
    else
        echo "Did NOT find WiringPi Version 2.36"
        # Check if the Dexter directory exists.
        DEXTER_DIR='/home/pi/Dexter'
        if [ -d "$DEXTER_DIR" ]; then
            # Will enter here if $DIRECTORY exists, even if it contains spaces
            echo "Dexter Directory Found!"
        else
            mkdir $DEXTER_DIR
        fi
        # Install wiringPi
        pushd $DEXTER_DIR   # Change directories to Dexter
        git clone https://github.com/DexterInd/wiringPi/  # Clone directories to Dexter.
        cd wiringPi
        sudo chmod +x ./build
        sudo ./build
        echo "wiringPi Installed"
        popd
    fi
    # End check if WiringPi installed
    echo " "
}

install_spi_i2c() {
    echo "Removing blacklist from /etc/modprobe.d/raspi-blacklist.conf . . ."
    echo "=================================================================="
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
    echo "Adding I2C-dev and SPI-dev in /etc/modules . . ."
    echo "================================================"
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
    echo "Making I2C changes in /boot/config.txt . . ."
    echo "================================================"

    echo dtparam=i2c1=on >> /boot/config.txt
    echo dtparam=i2c_arm=on >> /boot/config.txt

    sudo adduser pi i2c
    echo " "
}

install_arduino() {
    #Adding ARDUINO setup files
    echo " "
    echo "Making changes to Arduino . . ."
    echo "==============================="
    cd /tmp
    wget http://project-downloads.drogon.net/gertboard/avrdude_5.10-4_armhf.deb
    sudo dpkg -i avrdude_5.10-4_armhf.deb
    sudo chmod 4755 /usr/bin/avrdude

    cd /tmp
    wget http://project-downloads.drogon.net/gertboard/setup.sh
    chmod +x setup.sh
    sudo ./setup.sh

    #Enabling serial port in Arduino IDE
    crontab -l > file; echo '@reboot ln -sf /dev/ttyAMA0 /dev/ttyS0' >> file; crontab file
    rm file
    cd $ROBOT_DIR
    echo " "
}

call_for_reboot() {
    if ! called_from_di_update
    then
        echo " "
        echo "Please restart the Raspberry Pi for the changes to take effect"
        echo " "
        echo "Please restart to implement changes!"
        echo "  _____  ______  _____ _______       _____ _______ "
        echo " |  __ \|  ____|/ ____|__   __|/\   |  __ \__   __|"
        echo " | |__) | |__  | (___    | |  /  \  | |__) | | |   "
        echo " |  _  /|  __|  \___ \   | | / /\ \ |  _  /  | |   "
        echo " | | \ \| |____ ____) |  | |/ ____ \| | \ \  | |   "
        echo " |_|  \_\______|_____/   |_/_/    \_\_|  \_\ |_|   "
        echo " "
        echo "Please restart to implement changes!"
        echo "To Restart type sudo reboot"
    fi
}

############################################################################
############################################################################
identify_cie
identify_robot
check_root_user
display_welcome_msg
check_internet

SCRIPT_DIR="$(readlink -f $(dirname $0))"
ROBOT_DIR="${SCRIPT_DIR%/*}"
echo "Installing GoPiGo software in ${ROBOT_DIR}"
echo " "

install_dependencies


#Copy Software Servo
cp -R $ROBOT_DIR/Firmware/SoftwareServo/ /usr/share/arduino/libraries/

chmod +x gopigo 
cp gopigo /usr/bin

cd $ROBOT_DIR/Software/Python
python setup.py install
python3 setup.py install

install_DHT
install_wiringpi
install_spi_i2c

install_arduino

#sudo rm -r /tmp/di_update

sudo chmod +x $ROBOT_DIR/Software/Scratch/GoPiGo_Scratch_Scripts/*.sh

call_for_reboot
