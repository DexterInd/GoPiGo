#!/usr/bin/env python
#
# GoPiGo Example for using the Grove Temperature Sensor (http://www.seeedstudio.com/wiki/Grove_-_Temperature_Sensor)
#
# The GoPiGo is a robotics platform for the Raspberry Pi.  You can learn more about GoPiGo here:  www.dexterindustries.com/GoPiGo/
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/gopigo/
#
#
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2015  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
# NOTE: 
# 	The sensor uses a thermistor to detect ambient temperature.
# 	The resistance of a thermistor will increase when the ambient temperature decreases.
#	
# 	There are 3 revisions 1.0, 1.1 and 1.2, each using a different model thermistor.
# 	Each thermistor datasheet specifies a unique Nominal B-Constant which is used in the calculation forumla.
#	
# 	The second argument in the grovepi.temp() method defines which board version you have connected.
# 	Defaults to '1.0'. eg.
# 		temp = grovepi.temp(sensor)        # B value = 3975
# 		temp = grovepi.temp(sensor,'1.1')  # B value = 4250
# 		temp = grovepi.temp(sensor,'1.2')  # B value = 4250

import time
import math
from gopigo import analogRead

# Connect the Grove Temperature Sensor to Analog port A1
# The analog sensors won't work on any other port
# SIG,NC,VCC,GND
sensor = 15 # Analog Pin A1

def temp(pin, model = '1.0'):
	# each of the sensor revisions use different thermistors, each with their own B value constant
	if model == '1.2':
		bValue = 4250  # sensor v1.2 uses thermistor ??? (assuming NCP18WF104F03RC until SeeedStudio clarifies)
	elif model == '1.1':
		bValue = 4250  # sensor v1.1 uses thermistor NCP18WF104F03RC
	else:
		bValue = 3975  # sensor v1.0 uses thermistor TTC3A103*39H
	a = analogRead(pin)
	resistance = (float)(1023 - a) * 10000 / a
	t = (float)(1 / (math.log(resistance / 10000) / bValue + 1 / 298.15) - 273.15)
	return t
	
while True:
    try:
        tempr = temp(sensor,'1.1')
        print("temp =", tempr)
        time.sleep(.5)

    except KeyboardInterrupt:
        break
    except IOError:
        print ("Error")



