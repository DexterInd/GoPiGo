#!/usr/bin/env bash

PIHOME=/home/pi

DIUPDATE=di_update
RASPBIAN=Raspbian_For_Robots
RASPBIAN_PATH=$PIHOME/$DIUPDATE/$RASPBIAN

DEXTER=Dexter
DEXTER_PATH=$PIHOME/$DEXTER

GOPIGO_PATH=$DEXTER_PATH/GoPiGo

# setting quiet mode
if [[ -f /home/pi/quiet_mode ]]
then
        quiet_mode=1
else
        quiet_mode=0
fi

#######
# if we are NOT in quiet mode, then identify ourselves
#######

if [ $quiet_mode -eq 0 ]
then
	echo "  _____            _                                ";
	echo " |  __ \          | |                               ";
	echo " | |  | | _____  _| |_ ___ _ __                     ";
	echo " | |  | |/ _ \ \/ / __/ _ \ '__|                    ";
	echo " | |__| |  __/>  <| ||  __/ |                       ";
	echo " |_____/ \___/_/\_\\__\___|_| _        _            ";
	echo " |_   _|         | |         | |      (_)           ";
	echo "   | |  _ __   __| |_   _ ___| |_ _ __ _  ___  ___  ";
	echo "   | | | '_ \ / _\` | | | / __| __| '__| |/ _ \/ __|";
	echo "  _| |_| | | | (_| | |_| \__ \ |_| |  | |  __/\__ \ ";
	echo " |_____|_| |_|\__,_|\__,_|___/\__|_|  |_|\___||___/ ";
	echo "                                                    ";
	echo "                                                    ";
	echo " "

	printf "WELCOME TO IR RECEIVER SETUP FOR THE GOPIGO.\nPlease ensure internet connectivity before running this script.\nNOTE: Reboot Raspberry Pi after completion.\n"

	echo " "
	echo " "

	echo "Check for internet connectivity..."
	echo "=================================="
	wget -q --tries=2 --timeout=20 --output-document=/dev/null http://raspberrypi.org
	if [ $? -eq 0 ];then
		echo "Connected"
	else
		echo "Unable to Connect, try again !!!"
		exit 0
	fi

	sudo apt-get update -y
else
# being run from DI UPDATE
	printf "WELCOME TO IR RECEIVER SETUP FOR THE GOPIGO.\n"
fi

echo " "
echo "Installing Dependencies"
echo "======================="
sudo apt-get install lirc python-lirc -y

echo " "
echo "Copying Config Files"
echo "===================="
sudo cp $GOPIGO_PATH/Software/Python/ir_remote_control/script/hardware_copy.conf /etc/lirc/hardware.conf
sudo cp $GOPIGO_PATH/Software/Python/ir_remote_control/script/lircd_keyes.conf /etc/lirc/lircd.conf
sudo cp $GOPIGO_PATH/Software/Python/ir_remote_control/script/lircrc_keyes /etc/lirc/lircrc
echo "Files copied"


#####
# if we are not in quiet mode, then tell the user to restart

if [ $quiet_mode -eq 0 ]
then
	echo " "
	echo "Please restart the Raspberry Pi for the changes to take effect"
	echo "  _____  ______  _____ _______       _____ _______ "
	echo " |  __ \|  ____|/ ____|__   __|/\   |  __ \__   __|"
	echo " | |__) | |__  | (___    | |  /  \  | |__) | | |   "
	echo " |  _  /|  __|  \___ \   | | / /\ \ |  _  /  | |   "
	echo " | | \ \| |____ ____) |  | |/ ____ \| | \ \  | |   "
	echo " |_|  \_\______|_____/   |_/_/    \_\_|  \_\ |_|   "
	echo " "
	echo "To Restart type 'sudo reboot'"
fi
