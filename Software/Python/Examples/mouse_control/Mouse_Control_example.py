import struct
import sys
from gopigo import *
file = open( "/dev/input/mice", "rb" );

debug = 0
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
print "Press Enter to start"
a=raw_input()
fwd()
while( 1 ):
	[l,m,r,x,y]=getMouseEvent()
	if debug:
		print l,m,r,x,y
	if flag==1:
		fwd()
		flag=0
	if l:
		left()
		flag=1
	if m:
		stop()
	if r:
		right()
		flag=1
	if l and r:
		bwd()
