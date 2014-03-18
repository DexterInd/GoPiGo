import smbus
import time

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04
val=[0,0,0]
def analogRead():
	bus.read_byte(address)
	number = bus.read_i2c_block_data(address,1)
	val[0]= (float)(number[1]*256+number[2])
	val[1]= (float)(number[3]*256+number[4])
	val[2]= (float)(number[5]*256+number[6])
		
def writeNumber(value):
    bus.write_byte(address, value)
    # bus.write_byte_data(address, 0, value) 
    return -1

def readNumber():
    number = bus.read_byte(address)
    # number = bus.read_byte_data(address, 1)
    return number

time.sleep(1)
i=0
while True:
	a=analogRead()
	print "%.2f  "%(val[0]*5/1024),
	print "%.2f  "%(val[1]*5/1024),
	print "%.2f  "%(val[2]*5/1024)
	time.sleep(.1)
	
	
	
