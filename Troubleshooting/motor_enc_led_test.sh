#! /bin/bash
REPO_PATH=$(readlink -f $(dirname $0) | grep -E -o "^(.*?\\GoPiGo)")
echo ""
sudo python $REPO_PATH/Software/Python/tests/enc_tgt_test.py
