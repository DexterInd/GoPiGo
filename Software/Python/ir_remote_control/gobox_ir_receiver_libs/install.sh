#!/usr/bin/env bash
PIHOME=/home/pi

DIUPDATE=di_update
RASPBIAN=Raspbian_For_Robots
RASPBIAN_PATH=$PIHOME/$DIUPDATE/$RASPBIAN

DEXTER=Dexter
DEXTER_PATH=$PIHOME/$DEXTER

GOPIGO_PATH=$DEXTER_PATH/GoPiGo

#Install the ir_receiver library systemwide
pushd $GOPIGO_PATH/Software/Python/ir_remote_control/gobox_ir_receiver_libs/
sudo python setup.py install
sudo rm -r build
sudo rm -r dist
sudo rm -r ir_receiver.egg-info		

sudo chmod +x di_ir_reader_wrapper_monit.sh

popd
#https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-monit
sudo apt-get install monit -y

sudo cp  $GOPIGO_PATH/Software/Python/ir_remote_control/gobox_ir_receiver_libs/monitrc /etc/monit/monitrc
sudo monit start all 