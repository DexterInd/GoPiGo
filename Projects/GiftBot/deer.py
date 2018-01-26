#!/usr/bin/env python
from __future__ import print_function
from __future__ import division
from builtins import input

'''
Build a Present Delivery System.  Have a robot deliver your Christmas Presents!

https://www.dexterindustries.com/projects/giftbot-raspberry-pi-robot-delivers-christmas-gifts/

In this project, we'll show you GiftBot, the Raspberry Pi Robot that will deliver your Christmas Gifts and bring cheer to your holiday season.  We took the GoPiGo Raspberry Pi Robot, added some Jingle Bell Rock with the Raspberry Pi Speaker, and harnessed the power of three reindeer to deliver our gifts this year.  A elf will ride on the GoPiGo as it makes its rounds.

No reindeer robot would be complete without a Red Nosed Rudolf: we added one with a Red Grove LED!

## License
 GoPiGo for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
 Copyright (C) 2017  Dexter Industries

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
'''

from gopigo import *
import sys
import os
import subprocess
# from espeak import espeak
import atexit
atexit.register(stop)
led_pin = analogPort
pinMode(led_pin,"OUTPUT")


# Play some rock music.  You can play any mp3 for other sound file
# with omxplayer.  Change the full path name!
def play_rock():
	bashCommand = '''sudo omxplayer -o local /home/pi/rock.mp3'''
	print(bashCommand)
	subprocess.Popen(["sudo","omxplayer", "-o", "local", "/home/pi/rock.mp3"])  # Runs the bash command in the background.

# Blink Rudolfs Nose!
def blink(times):
	for each in range(0, times):
		try:
			digitalWrite(led_pin,1)
			time.sleep(.5)
			digitalWrite(led_pin,0)
			time.sleep(.5)

		except IOError:
			print ("Error")
	
while True:
	play_rock()
	fwd()
	blink(5)		# Adjust this rate for however long you want the GoPiGo to run!
