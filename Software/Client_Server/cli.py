#!/usr/bin/env python

# This is a basic example for a socket client for the GoPiGo.
# This connects to the GoPiGo socket server and can be used to send commands to run the GoPiGo
# the socket server is running on Port 5005 on localhost

# Send a single byte command to the server:
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
import time
def send(msg):
	TCP_IP = '127.0.0.1'
	TCP_PORT = 5005
	BUFFER_SIZE = 1024
	MESSAGE = msg
	
	#Create a socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#Connect to the server
	s.connect((TCP_IP, TCP_PORT))
	#Send the command
	s.send(MESSAGE)
	#Recieve response back
	data = s.recv(BUFFER_SIZE)
	s.close()
	return data
	

print send('f')
time.sleep(2)
print send('b')
time.sleep(2)
print send('l')
time.sleep(2)
print send('r')
time.sleep(2)
print send('s')