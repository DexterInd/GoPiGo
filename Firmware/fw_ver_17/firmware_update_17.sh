#! /bin/bash

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

   # Changing the fuses back to normal . . . could be a mistake

    sudo avrdude -c gpio -p m328p -U lfuse:w:0xFF:m
    sudo avrdude -c gpio -p m328p -U hfuse:w:0xDE:m
    sudo avrdude -c gpio -p m328p -U efuse:w:0x05:m

    avrdude -c gpio -p m328p -U flash:w:fw_ver_17.cpp.hex
    echo "============================="
else
  echo "Disconect your motors and retry!"
fi
