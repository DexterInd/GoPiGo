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
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)           
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
            if keyevent.keycode == 'BTN_A':
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

