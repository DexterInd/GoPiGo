#!/usr/bin/env python
#
# GoPiGo Example for using the analog read command to read analog sensor values like the Sound sensor(http://www.dexterindustries.com/shop/grove-sound-sensor/) and grove light sensor(http://www.dexterindustries.com/shop/grove-light-sensor/) 
#
# The GoPiGo is a robotics platform for the Raspberry Pi.  You can learn more about GoPiGo here:  www.dexterindustries.com/GoPiGo/
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/gopigo/
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

import time
import gopigo

# Connect the analog sensor like the sound sensor, light sensor, rotatary sensor to  A1
#   The pin should be 15 for A11 port or you can call the analogPort definitions from the GoPiGo library
#   The analog sensors won't work on any other port

sensor_pin = gopigo.analogPort
gopigo.pinMode(sensor_pin,"INPUT")
while True:
    try:
        print (gopigo.analogRead(sensor_pin))
        time.sleep(.5)

    except IOError:
        print ("Error")
