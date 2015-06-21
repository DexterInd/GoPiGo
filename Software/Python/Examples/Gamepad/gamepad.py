#!/usr/bin/python

###############################################################                                                                  
# This is the first script in the tutorial at
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

gamepad = InputDevice('/dev/input/event0')

speed=100
set_speed(speed)

for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        keyevent = categorize(event)
        if keyevent.keystate == KeyEvent.key_down:
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
                if speed > 550:
                    speed = 550
                set_speed(speed)
            elif keyevent.keycode == 'BTN_TL':
                print "Slower"
                speed -= 50
                if speed < 50:
                    speed = 50
                set_speed(speed)


