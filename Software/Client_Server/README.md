# GoPiGo Client Server

## This is a basic example for a socket-client server for the GoPiGo.
The example client server are written in Python.

The client can be easily ported to other languages since it's a basic client example and the python server can be run with python. This allows the GoPiGo to be portable to other languages easily without the need to write a basic library for the low level I2C commands.

The socket server accepts commands from the client and controls the GoPiGo
The socket server is running on Port 5005 on localhost

Send a single byte command to the server from the client:
	s 	- stop
	f 	- move forward
	b 	- move back
	l	- turn left
	r	- turn right
	
The server is just a very basic instance right now and we plan to expand it in the near future


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