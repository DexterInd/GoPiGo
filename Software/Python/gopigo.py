#!/usr/bin/python
import serial, time
import smbus
import math
import RPi.GPIO as GPIO
import struct
ser = serial.Serial('/dev/ttyAMA0',  9600, timeout = 0)

def fwd():
	send('w')
def bwd():
	send('s')
def left():
	send('a')
def right():
	send('d')
def stop():
	send('x')
def increase_speed():
	send('t')
def decrease_speed():
	send('g')
def volt():
	send('v')
	try:
		volt=ser.readline()
	except ser.SerialTimeoutException:
		print('Data could not be read')
	volt=int(volt)
	volt=(5*float(volt)/1024)/.4
	return volt
def us_dist(pin):
	send('u'+chr(pin))
	
	try:
		volt=ser.readline()
	except ser.SerialTimeoutException:
		print('Data could not be read')
	#volt=int(volt)
	return volt

def servo(position):
	send('b'+chr(position))
	
#if you only want to send data to arduino
def send( theinput ):
  ser.write( theinput )
  '''while True:
    try:
      time.sleep(0.01)
      break
    except:
      pass
  time.sleep(0.1)
'''
#if you would like to tell the arduino that you would like to receive data from the arduino
def send_and_receive( theinput ):
  ser.write( theinput )
  while True:
    try:
      time.sleep(0.01)
      state = ser.readline()
      return state
    except:
      pass
  time.sleep(0.1)