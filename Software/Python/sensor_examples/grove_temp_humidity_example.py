#!/usr/bin/env python
#
# GoPiGo Example for using the Grove Temperature & Humidity Sensor  
# (http://www.seeedstudio.com/wiki/Grove_-_Temperature_and_Humidity_Sensor)
#
# The GoPiGo is a robotics platform for the Raspberry Pi.  You can learn more about GoPiGo here:  www.dexterindustries.com/GoPiGo/
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/gopigo/
#
# This example is derived from the Adafruit_Python_DHT library https://github.com/adafruit/Adafruit_Python_DHT
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
import gopigo
import sys

# Connect the Grove Temperature & Humidity Sensor to the Serial Port on the GoPiGo
# This example uses the blue colored sensor.

# temp_humidity_sensor_type
blue = 0    # The Blue colored sensor.
white = 1   # The White colored sensor.

while True:
	try:
		# This example uses the blue colored sensor. 
		# The first parameter is the port, the second parameter is the type of sensor.
		[temp,humidity] = gopigo.dht(blue)  
		if temp ==-2.0 or humidity == -2.0:
			print ("Bad reading, trying again")
		elif temp ==-3.0 or humidity == -3.0:
			print ("Run the program as sudo")
			sys.exit()
		print("temp = %.02f C humidity =%.02f%%"%(temp, humidity))

	except IOError:
		print ("I2C Error")
