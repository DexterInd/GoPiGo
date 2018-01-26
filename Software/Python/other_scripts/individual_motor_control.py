#!/usr/bin/env python
# This is an example to test out the individual motors on the GoPiGo
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

import gopigo
import time

import atexit
atexit.register(gopigo.stop)

#Individual motor control:
# gopigo.motorX(dir,speed)
#		X: 		1 or 2 to control motor1 or motor2
#		dir:	1 for forward or 0 for back
#		speed:	0-255, 0 to stop and 255 for full speed

#Motor 1 control
print("Motor 1 moving forward at full speed")
gopigo.motor1(1,255)	
time.sleep(2)

print("Motor 1 moving forward at half speed")
gopigo.motor1(1,127)	
time.sleep(2)

print("Motor 1 stopping ")
gopigo.motor1(1,0)		
time.sleep(1)			# It is better to stop for a second before changing direction since it leads to less wear on the motors and less load on the power supply

print("Motor 1 moving back at full speed")
gopigo.motor1(0,255)	
time.sleep(2)

print("Motor 1 moving back at half speed")
gopigo.motor1(0,127)	
time.sleep(2)

print("Motor 1 stopping")
gopigo.motor1(1,0)		

#Motor 2 control
print("Motor 2 moving forward at full speed")
gopigo.motor2(1,255)	
time.sleep(2)

print("Motor 2 moving forward at half speed")
gopigo.motor2(1,127)	
time.sleep(2)

print("Motor 2 stopping ")
gopigo.motor2(1,0)	
time.sleep(1)

print("Motor 2 moving back at full speed")
gopigo.motor2(0,255)
time.sleep(2)

print("Motor 2 moving back at half speed")
gopigo.motor2(0,127)	
time.sleep(2)

print("Motor 2 stopping")
gopigo.motor2(1,0)		

spd=gopigo.read_motor_speed()
print ("Current speed M1:%d ,M2:%d " %(spd[0],spd[1]))
print("Changing speed")	

gopigo.set_speed(200)	# Setting motor speed to 200, so that the motors still move when the next program uses it

spd=gopigo.read_motor_speed()
print ("New speed M1:%d ,M2:%d " %(spd[0],spd[1]))