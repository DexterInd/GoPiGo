#!/usr/bin/env bash
update_gopigo_firmware(){ 
	sudo avrdude -c gpio -p m328p -U lfuse:w:0x7F:m
	sudo avrdude -c gpio -p m328p -U hfuse:w:0xDA:m
	sudo avrdude -c gpio -p m328p -U efuse:w:0x05:m
	# avrdude -c gpio -p m328p -U flash:w:/home/pi/Desktop/GoPiGo/Firmware/fw_ver_13.cpp.hex
	sudo avrdude -c gpio -p m328p -U flash:w:/home/pi/Desktop/GoPiGo/Firmware/fw_ver_16/fw_ver_16.cpp.hex
}