#! /bin/bash
curl --silent https://raw.githubusercontent.com/DexterInd/script_tools/master/install_script_tools.sh | bash

SCRIPT_DIR="$(readlink -f $(dirname $0))"
ROBOT_DIR="${SCRIPT_DIR%/*}"
PIHOME=/home/pi
DEXTERSCRIPT=$PIHOME/Dexter/lib/Dexter/script_tools

source $DEXTERSCRIPT/functions_library.sh

identify_cie() {
    if ! quiet_mode
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
feedback "Welcome to GoPiGo Installer."
echo " "
}

check_root_user() {
    if [[ $EUID -ne 0 ]]; then
        feedback "FAIL!  This script must be run as such: sudo ./install.sh"
        exit 1
    fi
    echo " "
}

check_internet() {
    if ! quiet_mode ; then
        feedback "Check for internet connectivity..."
        feedback "=================================="
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
    feedback "Please ensure internet connectivity before running this script."
    if ! quiet_mode
    then
        feedback "NOTE: Raspberry Pi will need to be rebooted after completion."
    fi

    feedback "Special thanks to Joe Sanford at Tufts University.  This script was derived from his work.  Thank you Joe!"
    echo " "
}

install_dependencies() {
    if ! quiet_mode ; then
        sudo apt-get update
    fi
    echo " "
    feedback "Installing Dependencies"
    feedback "======================="
    sudo apt-get install python-pip git libi2c-dev python-serial python-rpi.gpio i2c-tools python-smbus arduino minicom libnss-mdns python-dev -y
    sudo pip install -U RPi.GPIO
    sudo pip install pyusb
    sudo pip install numpy

    feedback "Dependencies installed"
}

install_DHT() {
    # Install the DHT library
    feedback "Installing DHT library"
    pushd $ROBOT_DIR/Software/Python/sensor_examples/dht/Adafruit_Python_DHT > /dev/null
    sudo python setup.py install
    sudo python3 setup.py install
    popd > /dev/null
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

    echo dtparam=i2c1=on >> /boot/config.txt
    echo dtparam=i2c_arm=on >> /boot/config.txt

    sudo adduser pi i2c
    echo " "
}

install_avr() {
    #Adding ARDUINO setup files
    echo " "
	######################################################################
	# Remove after the image is created for BrickPi3
	######################################################################
    # feedback "Making changes to Arduino . . ."
    # feedback "==============================="
    # cd /tmp
    # wget http://project-downloads.drogon.net/gertboard/avrdude_5.10-4_armhf.deb
    # sudo dpkg -i avrdude_5.10-4_armhf.deb
    # sudo chmod 4755 /usr/bin/avrdude
    # cd /tmp
    # if [ -f /tmp/setup.sh ]; then
        # rm /tmp/setup.sh
    # fi
    # wget http://project-downloads.drogon.net/gertboard/setup.sh
    # chmod +x setup.sh
    # sudo ./setup.sh
    # #Enabling serial port in Arduino IDE
    # crontab -l > file; echo '@reboot ln -sf /dev/ttyAMA0 /dev/ttyS0' >> file; crontab file
    # rm file
	######################################################################
	source /home/pi/Dexter/lib/Dexter/script_tools/install_avrdude.sh
	create_avrdude_folder
    install_avrdude
    cd $ROBOT_DIR
    echo "done with AVRDUDE "
}

install_line_follower(){
    feedback "--> Installing Line Follower Calibration"
    # Install GoPiGo Line Follower Calibration
    delete_file /home/pi/Desktop/line_follow.desktop
    sudo cp /home/pi/Dexter/GoPiGo/Software/Python/line_follower/line_follow.desktop /home/pi/Desktop/
    sudo chmod +x /home/pi/Desktop/line_follow.desktop
    sudo chmod +x /home/pi/Dexter/GoPiGo/Software/Python/line_follower/line_sensor_gui.py

    # if the configuration files exist in the home directory
    # then move them to their new place
    # otherwise create new ones
    if file_exists "$PIHOME/black_line.txt"
    then
        sudo mv $PIHOME/black_line.txt $PIHOME/Dexter/black_line.txt
    else
        sudo touch $PIHOME/Dexter/black_line.txt
    fi

    if file_exists "$PIHOME/white_line.txt"
    then
        sudo mv $PIHOME/white_line.txt $PIHOME/Dexter/white_line.txt
    else
        sudo touch $PIHOME/Dexter/white_line.txt
    fi
    if file_exists "$PIHOME/range_line.txt"
    then
        sudo mv $PIHOME/range_line.txt $PIHOME/Dexter/range_line.txt
    else
        sudo touch $PIHOME/Dexter/range_line.txt
    fi

    sudo chmod 666 $PIHOME/Dexter/*line.txt

}

install_control_panel(){
    sudo cp "$ROBOT_DIR/Software/Python/control_panel/gopigo_control_panel.desktop" $PIHOME/Desktop
}

call_for_reboot() {
    if ! quiet_mode ; then
        feedback " "
        feedback "Please restart the Raspberry Pi for the changes to take effect"
        feedback " "
        feedback "Please restart to implement changes!"
        feedback "  _____  ______  _____ _______       _____ _______ "
        feedback " |  __ \|  ____|/ ____|__   __|/\   |  __ \__   __|"
        feedback " | |__) | |__  | (___    | |  /  \  | |__) | | |   "
        feedback " |  _  /|  __|  \___ \   | | / /\ \ |  _  /  | |   "
        feedback " | | \ \| |____ ____) |  | |/ ____ \| | \ \  | |   "
        feedback " |_|  \_\______|_____/   |_/_/    \_\_|  \_\ |_|   "
        feedback " "
        feedback "Please restart to implement changes!"
        feedback "To Restart type sudo reboot"
    fi
}

############################################################################
############################################################################
identify_cie
identify_robot
check_root_user
display_welcome_msg
check_internet

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
install_avr
install_line_follower
install_control_panel

#sudo rm -r /tmp/di_update

sudo chmod +x $ROBOT_DIR/Software/Scratch/GoPiGo_Scratch_Scripts/*.sh

call_for_reboot
