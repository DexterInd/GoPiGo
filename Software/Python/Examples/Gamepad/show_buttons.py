#!/usr/bin/python

###############################################################                                                                  
# Displays gamepad button keycodes
#
# History
# ------------------------------------------------
# Author                Date      		Comments
# Eric Goebelbecker     Jun 6 2015 		Initial Authoring
# 			                                                         
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)           
#
###############################################################
from select import select
from evdev import InputDevice, categorize, ecodes, KeyEvent
gamepad = InputDevice('/dev/input/event0')

for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        keyevent = categorize(event)
        if keyevent.keystate == KeyEvent.key_down:
            print keyevent.keycode

