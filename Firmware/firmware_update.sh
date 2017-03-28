#!/usr/bin/env bash

REPO_PATH=$(readlink -f $(dirname $0) | grep -E -o "^(.*?\\GoPiGo)")
 
if [ "$(whoami)" != 'root' ]; then
        echo "You have no permission to run $0 as non-root user."
        echo "Run using sudo and try again."
        exit 1;
fi

echo "ATTENTION! Important!"
echo "BEFORE PROGRAMMING THE GOPIGO FIRMWARE, DISCONNECT THE MOTORS."
echo "Please confirm that you've disconnected the motors."
echo "Have you disconnected the motors before programming the firmware? (y/n)"

read motors
y='y'

if [ $motors = $y ]; then
	echo "Updating the GoPiGo firmware"
	echo "============================="

	data='date'
	now=$($data)
	echo "$now"

	source $REPO_PATH/Firmware/gopigo_firmware_update.sh
	update_gopigo_firmware
	echo "=============================" 
else
  echo "Disconect your motors and retry!"
fi
