#! /bin/bash

echo =============================
echo GoPiGo Troubleshooting Script
echo ============================= 

echo ""
echo Adding permissions to the scripts
echo ================================= 
cd /home/pi/Desktop/GoPiGo/Troubleshooting/
chmod +x software_status.sh
chmod +x avrdude_test.sh
chmod +x i2c_test1.sh
chmod +x firmware_version_test.sh
chmod +x motor_enc_led_test.sh

sudo ./software_status.sh 2>&1| tee log.txt 
sudo ./avrdude_test.sh 2>&1| tee -a log.txt 
sudo ./i2c_test1.sh 2>&1| tee -a log.txt 
sudo ./firmware_version_test.sh 2>&1| tee -a log.txt  
sudo ./motor_enc_led_test.sh 2>&1| tee -a log.txt  

cp log.txt /home/pi/Desktop/log.txt

if [ ! -f /home/pi/cinch ]; then
    echo "No Cinch Found."
else
    feedback "Found cinch, running wifi debug install."
    pushd /home/pi/di_update/Raspbian_For_Robots/Troubleshooting_GUI
	sudo bash wifi_debug_info.sh
	cat wireless-info.txt >> /home/pi/Desktop/log.txt
	sudo cp /home/pi/Desktop/log.txt /boot
	popd
fi

echo "Log has been saved to Desktop. Please copy it and send it by email or upload it on the forums"
