#!/usr/bin/env python
# This script is to test the encoder values from the GoPiGo
from gopigo import *
import sys

import atexit
atexit.register(stop)

fwd()
time.sleep(1)
while True:
	print enc_read(0),
	print enc_read(1)