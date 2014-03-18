import smbus
import time
from subprocess import call

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04

def writeNumber(value):
    bus.write_byte(address, value)
    # bus.write_byte_data(address, 0, value) 
    return -1

def readNumber():
    number = bus.read_byte(address)
    # number = bus.read_byte_data(address, 1)
    return number
	
def sound(spk):
	cmd_beg="espeak --stdout '"
	cmd_end="' | aplay"
	print cmd_beg+spk+cmd_end
	call ([cmd_beg+spk+cmd_end], shell=True)

time.sleep(1)
i=0
while True:
	try:
		a=raw_input()
		print ord(a)
		writeNumber(ord(a))
		if a=='w':
			sound("Forward")
		elif a=='a':
			sound("Left")
		elif a=='d':
			sound("Right")
		elif a=='s':
			sound("Reverse")
		elif a=='x':
			sound("Stop")
	except IOError:
		print "Error"
	
	
	
