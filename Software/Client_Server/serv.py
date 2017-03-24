#!/usr/bin/env python 

# This is a basic example for a socket server for the GoPiGo.
# This allows the client to connects can be used to respond to the commands and run the GoPiGo
# the socket server is running on Port 5005 on localhost

# Send a single byte command to the server from the client:
#	s 	- stop
#	f 	- move forward
#	b 	- move back
#	l	- turn left
#	r	- turn right

'''
## License
 GoPiGo for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
 Copyright (C) 2017  Dexter Industries

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
'''

import socket
import gopigo

# Listen on localhost at port 5005
TCP_IP = '127.0.0.1' 
TCP_PORT = 5005
BUFFER_SIZE = 20

# Create a TCP socket and bind the server to the port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
print "Server Started"

while True:
	#Wait for incomming connections
	s.listen(1)
	
	#Accept an incoming connection
	conn, addr = s.accept()
	
	print '\nConnection address:', addr
	while 1:
		#Check the data
		data = conn.recv(BUFFER_SIZE)
		if not data: break	
		print "received data:", data
		if len(data) <> 1:
			print ("Invalid command")
			conn.send("Invalid command")
		elif data=='f':
			gopigo.fwd()
			conn.send("Moving forward")
		elif data=='s':
			gopigo.stop()
			conn.send("Stopping")
		elif data=='b':
			gopigo.bwd()
			conn.send("Moving back")
		elif data=='l':
			gopigo.left()
			conn.send("Turning left")
		elif data=='r':
			gopigo.right()
			conn.send("Turning right")
		else:
			print ("Invalid command")
			conn.send("Invalid command")
	conn.close()