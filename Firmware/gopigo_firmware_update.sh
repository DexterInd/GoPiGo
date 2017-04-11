#!/usr/bin/env bash
REPO_PATH=$(readlink -f $(dirname $0) | grep -E -o "^(.*?\\GoPiGo)")
update_gopigo_firmware(){ 
	# Check if this function is called from a Dexter script like
	# /Raspbian_For_Robots/upd_script/update_GoPiGo_Firmware.sh
	if [[ "$1" == "Dexter" ]]
	then
	    REPO_PATH=/home/pi/Dexter/GoPiGo
	fi
	# Checking if the REPO_PATH contains GoPiGo folder
	if ! echo "$REPO_PATH" | grep -q "/GoPiGo"
	then
	    echo "Error in REPO_PATH:$REPO_PATH"
	    exit
	fi
	echo "GoPiGo is found at :$REPO_PATH"
	sudo avrdude -c gpio -p m328p -U lfuse:w:0x7F:m
	sudo avrdude -c gpio -p m328p -U hfuse:w:0xDA:m
	sudo avrdude -c gpio -p m328p -U efuse:w:0x05:m
	# avrdude -c gpio -p m328p -U flash:w:/home/pi/Desktop/GoPiGo/Firmware/fw_ver_13.cpp.hex
	sudo avrdude -c gpio -p m328p -U flash:w:$REPO_PATH/Firmware/fw_ver_16/fw_ver_16.cpp.hex
}
