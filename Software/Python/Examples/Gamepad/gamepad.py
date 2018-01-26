#!/usr/bin/python

###############################################################                                                                  
# Find details on this script at
# http://wp.me/p5kNk-37
#
# History
# ------------------------------------------------
# Author                Date      		Comments
# Eric Goebelbecker     Jun 6 2015 		Initial Authoring
# 			                                                         
'''
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
#
###############################################################
from evdev import InputDevice, categorize, ecodes, KeyEvent
from gopigo import *

# Open the device
gamepad = InputDevice('/dev/input/event0')

# Set our initial speed
speed=100
set_speed(speed)

#
# The keycodes here work with a Logitech F710 Gamepad
# If your gamepad does not work use show_buttons.py
# to find the code you wish to use and replace them in 
# this if/elif block
#
for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        keyevent = categorize(event)
        if keyevent.keystate == KeyEvent.key_down:
            # BTN_A comes in a tuple
            if keyevent.keycode[0] == 'BTN_A':
                print "Back"
                bwd()
            elif keyevent.keycode == 'BTN_Y':
                print "Forward"
                fwd()
            elif keyevent.keycode == 'BTN_B':
                print "Right"
                right()
            elif keyevent.keycode == 'BTN_X':
                print "Left"
                left()
            elif keyevent.keycode == 'BTN_THUMBR' or keyevent.keycode == 'BTN_THUMBL':
                print "Stop"
                stop()
            elif keyevent.keycode == 'BTN_TR':
                print "Faster"
                speed += 50
                if speed > 250:
                    speed = 250
                set_speed(speed)
            elif keyevent.keycode == 'BTN_TL':
                print "Slower"
                speed -= 50
                if speed < 50:
                    speed = 50
                set_speed(speed)

