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

else
# being run from DI UPDATE
	printf "WELCOME TO IR RECEIVER SETUP FOR THE GOPIGO.\n"
fi

echo " "
echo "Copying Config Files"
echo "===================="
sudo cp $GOPIGO_PATH/Software/Python/ir_remote_control/lirc/hardware_copy.conf /etc/lirc/hardware.conf
sudo cp $GOPIGO_PATH/Software/Python/ir_remote_control/lirc/lircd_keyes.conf /etc/lirc/lircd.conf
sudo cp $GOPIGO_PATH/Software/Python/ir_remote_control/lirc/lircrc_keyes /etc/lirc/lircrc
echo "Lirc files copied"
