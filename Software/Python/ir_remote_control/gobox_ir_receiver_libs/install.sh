#!/usr/bin/env bash

#Install the ir_receiver library systemwide
sudo python /home/pi/Desktop/GoPiGo/Software/Python/ir_remote_control/gobox_ir_receiver_libs/setup.py install
sudo rm -r /home/pi/Desktop/GoPiGo/Software/Python/ir_remote_control/gobox_ir_receiver_libs/build
sudo rm -r /home/pi/Desktop/GoPiGo/Software/Python/ir_remote_control/gobox_ir_receiver_libs/dist
sudo rm -r /home/pi/Desktop/GoPiGo/Software/Python/ir_remote_control/gobox_ir_receiver_libs/ir_receiver.egg-info		

sudo chmod +x di_ir_reader_wrapper_monit.sh

#https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-monit
sudo apt-get install monit

sudo cp monitrc /etc/monit/monitrc
sudo monit start all