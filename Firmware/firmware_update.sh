#! /bin/bash
echo "Updating the GoPiGo firmware"
echo "============================="
avrdude -c gpio -p m328p -U flash:w:fw_ver_10.cpp.hex
gpg
