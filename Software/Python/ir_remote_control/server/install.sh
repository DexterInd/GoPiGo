#!/usr/bin/env bash
PIHOME=/home/pi

DIUPDATE=di_update
RASPBIAN=Raspbian_For_Robots
RASPBIAN_PATH=$PIHOME/$DIUPDATE/$RASPBIAN

DEXTER=Dexter
DEXTER_PATH=$PIHOME/$DEXTER

GOPIGO_PATH=$DEXTER_PATH/GoPiGo

#Install the ir_receiver library systemwide
pushd $GOPIGO_PATH/Software/Python/ir_remote_control/server/
python setup.py install
rm -r build
rm -r dist
rm -r ir_receiver.egg-info

sudo cp ir-server.service /etc/systemd/system/ir-server.service
sudo systemctl daemon-reload

popd
