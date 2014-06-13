from gopigo import *
import struct

file = open( "/dev/input/mice", "rb" );
last_x = 0;
last_y = 0;


def getMouseEvent():
  buf = file.read(3);
  button = ord( buf[0] );
  bLeft = button & 0x1;
  bMiddle = ( button & 0x4 ) > 0;
  bRight = ( button & 0x2 ) > 0;
  x,y = struct.unpack( "bb", buf[1:] );
  print ("L:%d, M: %d, R: %d, x: %d, y: %d\n" % (bLeft,bMiddle,bRight, x, y) );
  # Now move the wheels according to the moues movements.
  if x == last_x:
	stop()
  if x > 0:
	right()
  if x < 0:
	left()

  return 
  

while True:
	# a=raw_input()
	'''if a=='w':
		fwd()
	elif a=='a':
		left()
	elif a=='d':
		right()
	elif a=='s':
		bwd()
	elif a=='x':
		stop()
	elif a=='t':
		increase_speed()
	elif a=='g':
		decrease_speed()
	elif a=='v':
		print volt(),'V'
	elif a=='u':
		print us_dist(17)
	elif a=='b': #servo test
		for i in range(180):
			servo(i)
			time.sleep(.02)
	time.sleep(.1)
	'''
	getMouseEvent()
	
	time.sleep(.1)
	