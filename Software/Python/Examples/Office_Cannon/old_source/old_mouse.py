#!/usr/bin/python
########################################################################                                                                  
# This example controls the GoPiGo and Rocket Launcher with a wireless mouse on the USB port.
# The GoPiGo motion is controlled by moving the mouse.
# The Rocket Launcher is controlled by pressing the mouse left button, and moving the mouse.
# The Rocket Launcher is fired by pressing the middle button.  
#                                
# http://www.dexterindustries.com/GoPiGo/                                                                
# History
# ------------------------------------------------
# Author     Date      		Comments
# John Cole  April 14  		Initial Authoring                                                            
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)           
#
########################################################################
from gopigo import *
import struct

import sys
import platform
import time
import socket
import re
import json
import urllib2
import base64

import usb.core
import usb.util

# Protocol command bytes
DOWN    = 0x01
UP      = 0x02
LEFT    = 0x04
RIGHT   = 0x08
FIRE    = 0x10
STOP    = 0x20

DEVICE = None
DEVICE_TYPE = None

file = open( "/dev/input/mice", "rb" );


def setup_usb():
    # Tested only with the Cheeky Dream Thunder
    # and original USB Launcher
    global DEVICE 
    global DEVICE_TYPE

    DEVICE = usb.core.find(idVendor=0x2123, idProduct=0x1010)

    if DEVICE is None:
        DEVICE = usb.core.find(idVendor=0x0a81, idProduct=0x0701)
        if DEVICE is None:
            raise ValueError('Missile device not found')
        else:
            DEVICE_TYPE = "Original"
    else:
        DEVICE_TYPE = "Thunder"

    

    # On Linux we need to detach usb HID first
    if "Linux" == platform.system():
        try:
            DEVICE.detach_kernel_driver(0)
        except Exception, e:
            pass # already unregistered    

    DEVICE.set_configuration()


def send_cmd(cmd):
    if "Thunder" == DEVICE_TYPE:
        DEVICE.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, cmd, 0x00,0x00,0x00,0x00,0x00,0x00])
    elif "Original" == DEVICE_TYPE:
        DEVICE.ctrl_transfer(0x21, 0x09, 0x0200, 0, [cmd])

def led(cmd):
    if "Thunder" == DEVICE_TYPE:
        DEVICE.ctrl_transfer(0x21, 0x09, 0, 0, [0x03, cmd, 0x00,0x00,0x00,0x00,0x00,0x00])
    elif "Original" == DEVICE_TYPE:
        print("There is no LED on this device")

def send_move(cmd, duration_ms):
    send_cmd(cmd)
    time.sleep(duration_ms / 1000.0)
    send_cmd(STOP)


def run_command(command, value):
    command = command.lower()
    if command == "right":
        send_move(RIGHT, value)
    elif command == "left":
        send_move(LEFT, value)
    elif command == "up":
        send_move(UP, value)
    elif command == "down":
        send_move(DOWN, value)
    elif command == "zero" or command == "park" or command == "reset":
        # Move to bottom-left
        send_move(DOWN, 2000)
        send_move(LEFT, 8000)
    elif command == "pause" or command == "sleep":
        time.sleep(value / 1000.0)
    elif command == "led":
        if value == 0:
            led(0x00)
        else:
            led(0x01)
    elif command == "fire" or command == "shoot":
        if value < 1 or value > 4:
            value = 1
        # Stabilize prior to the shot, then allow for reload time after.
        time.sleep(0.5)
        for i in range(value):
            send_cmd(FIRE)
            time.sleep(4.5)
    else:
        print "Error: Unknown command: '%s'" % command


def run_command_set(commands):
    for cmd, value in commands:
        run_command(cmd, value)


def getMouseEvent():
  buf = file.read(3);
  button = ord( buf[0] );
  bLeft = button & 0x1;
  bMiddle = ( button & 0x4 ) > 0;
  bRight = ( button & 0x2 ) > 0;
  x,y = struct.unpack( "bb", buf[1:] );
  # print ("L:%d, M: %d, R: %d, x: %d, y: %d\n" % (bLeft,bMiddle,bRight, x, y) );
  # Now move the wheels according to the moues movements.

  if bMiddle > 0:
	print "fire rockets"
	run_command("fire", 100)

  if bLeft > 0:
	stop()
	if math.fabs(x) > math.fabs(y):
		if x == 0:
			print "Stop rockets"
		elif x > 0:
			print "Left rockets"
			run_command("left", 100)
		elif x < 0:
			print "Right rockets"
			run_command("right", 100)
	else:
		if y == 0:
			print "Stop Rockets Y"
		elif y > 0:
			print "Up Rockets"
			run_command("up", 100)
		elif y < 0:
			print "Down rockets"
			run_command("down", 100)
  else:
	if math.fabs(x) > math.fabs(y):
  		if x == 0:
			stop()
			run_command("led", 1)
			run_command("led", 0)
		elif x > 0:
			right()
		elif x < 0:
			left()
	else:
		if y == 0:
			stop()
			run_command("led", 1)
			run_command("led", 0)
		elif y > 0:
			fwd()
		elif y < 0:
			bwd()
  return 

setup_usb()
run_command("zero", 5000)
  
while True:
	getMouseEvent()
	time.sleep(.1)
	
