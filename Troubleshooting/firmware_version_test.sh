#! /bin/bash
REPO_PATH=$(readlink -f $(dirname $0) | grep -E -o "^(.*?\\GoPiGo)")
echo ""
echo Checking for firmware version and CPU Speed and Voltage
echo =======================================================
sudo python $REPO_PATH/Software/Python/tests/firmware_version_cpu_test.py
