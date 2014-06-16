# This example controls the GoPiGo and Rocket Launcher with a wireless mouse on the USB port.
# The GoPiGo motion is controlled by using the buttons.
# The Rocket Launcher is controlled by moving the mouse.
# The Rocket Launcher is fired by pressing the middle button.  

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
debug = 0

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
  buf = file.read(3)
  button = ord( buf[0] )
  bLeft = button & 0x1
  bMiddle = ( button & 0x4 ) > 0
  bRight = ( button & 0x2 ) > 0
  x,y = struct.unpack( "bb", buf[1:] )
  if debug:
    print ("L:%d, M: %d, R: %d, x: %d, y: %d\n" % (bLeft,bMiddle,bRight, x, y) )
  return [bLeft,bMiddle,bRight,x,y]
flag=0
def control():
  global flag
  #buf = file.read(3);
  #button = ord( buf[0] );
  #bLeft = button & 0x1;
  #bMiddle = ( button & 0x4 ) > 0;
  #bRight = ( button & 0x2 ) > 0;
  #x,y = struct.unpack( "bb", buf[1:] );
  # print ("L:%d, M: %d, R: %d, x: %d, y: %d\n" % (bLeft,bMiddle,bRight, x, y) );
  # Now move the wheels according to the moues movements.

  [bLeft,bMiddle,bRight,x,y]=getMouseEvent()  #Get the inputs from the mouse
  
  #if debug:
  #print bLeft,bMiddle,bRight,x,y
    
  if flag==1: #If left or right mouse not pressed, move forward
    fwd()
    flag=0
  if bLeft:    #If left mouse buton pressed, turn left
    left()
    flag=1
  #if bMiddle:    #If middle mouse button pressed, stop
    #stop()
  if bRight:    #If right mouse button presses, turn right
    right()
    flag=1
  if bLeft and bRight:  #If both the left and right mouse buttons pressed, go back
    #bwd()
	stop()
	flag=0
 
  tdelay=80
  if bMiddle > 0:
    print "fire rockets"
    run_command("fire", tdelay)

  #if bLeft > 0:
  #  stop()
    #if math.fabs(x) > math.fabs(y):
  if x == 0:
    print "Stop rockets"
  elif x > 10:
    print "Left rockets"
    run_command("left", tdelay)
  elif x < -10:
    print "Right rockets"
    run_command("right", tdelay)
  #else:
  if y == 0:
    print "Stop Rockets Y"
  elif y > 10:
    print "Up Rockets"
    run_command("up", tdelay)
  elif y < -10:
    print "Down rockets"
    run_command("down", tdelay)
  #else:
    #if math.fabs(x) > math.fabs(y):
     # if x == 0:
      #  stop()
       # run_command("led", 1)
        #run_command("led", 0)
    #elif x > 0:
    #  right()
    #elif x < 0:
    #  left()
    #else:
     # if y == 0:
      
#	  stop()
 #       run_command("led", 1)
  #      run_command("led", 0)
    #elif y > 0:
    #  fwd()
    #elif y < 0:
    #  bwd()
  return 

print "Setting up"
print "Left Mouse button- Turn left\nRight mouse button- Turn right\nBoth left and right- Stop\nMiddle mouse button- Fire rocket\nMove mouse to control the launcher"
setup_usb()
run_command("zero", 100)
print "Start\n............."
while True:
  control()
  
