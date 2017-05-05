#!/usr/bin/env python
from __future__ import print_function
from __future__ import division
from builtins import input

import sys
import tty
import select
import time
import gopigo
import numpy
import math
import threading
from datetime import datetime

from multiprocessing import Process, Lock

try:
    sys.path.insert(0, '/home/pi/Dexter/GoPiGo/Software/Python/line_follower')
    import line_sensor
    import scratch_line
    is_line_follower_accessible = True
except:
    try:
        sys.path.insert(0, '/home/pi/GoPiGo/Software/Python/line_follower')
        import line_sensor
        import scratch_line
        is_line_follower_accessible = True
    except:
        is_line_follower_accessible = False

old_settings = ''
fd = ''
##########################

read_is_open = True
global_lock = None

def debug(in_str):
    if False:
        print(in_str)

def create_lock():
    global global_lock
    # print("Creating Lock")
    global_lock = Lock()
    # print("easy lock is {}".format(global_lock))
    return global_lock

def set_lock(in_lock):
    global global_lock
    # print("Setting Lock")
    global_lock = in_lock
    print(global_lock)

def get_lock():
    return global_lock

def _grab_read():
    global global_lock
    status = False
    try:
        status = global_lock.acquire(timeout=1)
    except:
        pass
    return status
    # print("acquired")

def _release_read():
    global global_lock
    try:
        global_lock.release()
    except:
        pass
    # print("released")


def volt():
    voltage = 0
    if _grab_read():
        voltage = gopigo.volt()
        _release_read()
    return voltage

def stop():
    _grab_read()
    gopigo.stop()
    _release_read()

def backward():
    _grab_read()
    gopigo.backward()
    _release_read()

def left():
    _grab_read()
    gopigo.left()
    _release_read()

def right():
    _grab_read()
    gopigo.right()
    _release_read()

def forward():
    _grab_read()
    gopigo.forward()
    _release_read()


#############################################################
# the following is in a try/except structure because it depends
# on the date of gopigo.py
#############################################################
try:
    PORTS = {"A1": gopigo.analogPort, "D11": gopigo.digitalPort,
             "SERIAL": -1, "I2C": -2}
except:
    PORTS = {"A1": 15, "D11": 10, "SERIAL": -1, "I2C": -2}


ANALOG = 1
DIGITAL = 0
SERIAL = -1
I2C = -2

##########################


class Sensor():
    '''
    Base class for all sensors
    Class Attributes:
        port : string - user-readable port identification
        portID : integer - actual port id
        pinmode : "INPUT" or "OUTPUT"
        pin : 1 for ANALOG, 0 for DIGITAL
        descriptor = string to describe the sensor for printing purposes
    Class methods:
        setPort / getPort
        setPinMode / getPinMode
        isAnalog
        isDigital
    '''
    def __init__(self, port, pinmode):
        '''
        port = one of PORTS keys
        pinmode = "INPUT", "OUTPUT", "SERIAL" (which gets ignored)
        '''
        debug("Sensor init")
        debug(pinmode)
        self.setPort(port)
        self.setPinMode(pinmode)
        if pinmode == "INPUT" or pinmode == "OUTPUT":
            gopigo.pinMode(self.getPortID(), self.getPinMode())

    def __str__(self):
        return ("{} on port {}".format(self.descriptor, self.getPort()))

    def setPort(self, port):
        self.port = port
        self.portID = PORTS[self.port]

    def getPort(self):
        return (self.port)

    def getPortID(self):
        return (self.portID)

    def setPinMode(self, pinmode):
        self.pinmode = pinmode

    def getPinMode(self):
        return (self.pinmode)

    def isAnalog(self):
        return (self.pin == ANALOG)

    def isDigital(self):
        return (self.pin == DIGITAL)

    def set_descriptor(self, descriptor):
        self.descriptor = descriptor
##########################


class DigitalSensor(Sensor):
    '''
    Implements read and write methods
    '''
    def __init__(self, port, pinmode):
        debug("DigitalSensor init")
        self.pin = DIGITAL
        Sensor.__init__(self, port, pinmode)

    def read(self):
        '''
        tries to get a value up to 10 times.
        As soon as a valid value is read, it returns either 0 or 1
        returns -1 after 10 unsuccessful tries
        '''
        okay = False
        error_count = 0

        _grab_read()
        while not okay and error_count < 10:
            try:
                rtn = int(gopigo.digitalRead(self.getPortID()))
                okay = True
            except:
                error_count += 1
        _release_read()
        if error_count > 10:
            return -1
        else:
            return rtn

    def write(self, power):
        self.value = power
        return gopigo.digitalWrite(self.getPortID(), power)
##########################


class AnalogSensor(Sensor):
    '''
    implements read and write methods
    '''
    def __init__(self, port, pinmode):
        debug("AnalogSensor init")
        self.value = 0
        self.pin = ANALOG
        Sensor.__init__(self, port, pinmode)

    def read(self):
        _grab_read()
        self.value = gopigo.analogRead(self.getPortID())
        _release_read()
        return self.value

    def percent_read(self):
        return self.read * 100 / 1024

    def write(self, power):
        self.value = power
        return gopigo.analogWrite(self.getPortID(), power)
##########################


class LightSensor(AnalogSensor):
    """
    Creates a light sensor from which we can read.
    Light sensor is by default on pin A1(A-one)
    self.pin takes a value of 0 when on analog pin (default value)
        takes a value of 1 when on digital pin
    """
    def __init__(self, port="A1", gpg=None):
        debug("LightSensor init")
        AnalogSensor.__init__(self, port, "INPUT")
        self.set_descriptor("Light sensor")
##########################


class SoundSensor(AnalogSensor):
    """
    Creates a sound sensor
    """
    def __init__(self, port="A1",gpg=None):
        debug("Sound Sensor on port "+port)
        AnalogSensor.__init__(self, port, "INPUT")
        self.set_descriptor("Sound sensor")

##########################


class UltraSonicSensor(AnalogSensor):

    def __init__(self, port="A1",gpg=None):
        debug("Ultrasonic Sensor on port "+port)
        AnalogSensor.__init__(self, port, "INPUT")
        self.safe_distance = 500
        self.set_descriptor("Ultrasonic sensor")

    def is_too_close(self):
        _grab_read()
        if gopigo.us_dist(PORTS[self.port]) < self.get_safe_distance():
            _release_read()
            return True

        _release_read()
        return False

    def set_safe_distance(self, dist):
        self.safe_distance = int(dist)

    def get_safe_distance(self):
        return self.safe_distance

    def read(self):
        '''
        Limit the ultrasonic sensor to a distance of 5m.
        Take 3 readings, discard any that's higher than 3m
        If we discard 5 times, then assume there's nothing in front
            and return 501
        '''
        return_reading = 0
        readings =[]
        skip = 0
        while len(readings) < 3:
            _grab_read()
            value = gopigo.corrected_us_dist(PORTS[self.port])
            _release_read()
            if value < 300 and value > 0:
                readings.append(value)
            else:
                skip +=1
                if skip > 5:
                    break

        if skip > 5:
            return(501)

        for reading in readings:
            return_reading += reading

        return_reading = int(return_reading // len(readings))

        return (return_reading)


    def read_inches(self):
        value = self.read()
        return (value / 2.54)
##########################


class Buzzer(AnalogSensor):
    '''
    The Buzzer class is a digital Sensor with power modulation (PWM).
    Default port is D11
    Note that it inherits from AnalogSensor in order to support PWM
    It has three methods:
    sound(power)
    soundoff() -> which is the same as sound(0)
    soundon() -> which is the same as sound(254), max value
    '''
    def __init__(self, port="D11",gpg=None):
        AnalogSensor.__init__(self, port, "OUTPUT")
        self.set_descriptor("Buzzer")
        self.power = 254

    def sound(self, power):
        '''
        sound takes a power argument (from 0 to 254)
        the power argument will accept either a string or a numeric value
        if power can't be cast to an int, then turn buzzer off
        '''
        try:
            power = int(power)
        except:
            power = 0

        if power < 0:
            power = 0
        self.power = power
        AnalogSensor.write(self, power)

    def sound_off(self):
        '''
        Makes buzzer silent
        '''
        self.power = 0
        AnalogSensor.write(self, 0)

    def sound_on(self):
        '''
        Maximum buzzer sound
        '''
        self.power = 254
        AnalogSensor.write(self, 254)
##########################


class Led(AnalogSensor):
    def __init__(self, port="D11",gpg=None):
        AnalogSensor.__init__(self, port, "OUTPUT")
        self.set_descriptor("LED")

    def light_on(self, power):
        AnalogSensor.write(self, power)
        self.value = power

    def light_off(self):
        AnalogSensor.write(self, 0)

    def is_on(self):
        return (self.value > 0)

    def is_off(self):
        return (self.value == 0)
##########################


class MotionSensor(DigitalSensor):
    def __init__(self, port="D11",gpg=None):
        DigitalSensor.__init__(self, port, "INPUT")
        self.set_descriptor("Motion Sensor")
##########################


class ButtonSensor(DigitalSensor):

    def __init__(self, port="D11",gpg=None):
        DigitalSensor.__init__(self, port, "INPUT")
        self.set_descriptor("Button sensor")
##########################


class Remote(Sensor):

    def __init__(self, port="SERIAL",gpg=None):
        global IR_RECEIVER_ENABLED
        # IR Receiver
        try:
            import ir_receiver
            import ir_receiver_check
            IR_RECEIVER_ENABLED = True
        except:
            IR_RECEIVER_ENABLED = False

        if ir_receiver_check.check_ir() == 0:
            print("*** Error with the Remote Controller")
            print("Please enable the IR Receiver in the Advanced Comms tool")
            IR_RECEIVER_ENABLED = False
        else:
            Sensor.__init__(self, port, "SERIAL")
            self.set_descriptor("Remote Control")

    def is_enabled(self):
        return IR_RECEIVER_ENABLED

    def get_remote_code(self):
        '''
        Returns the keycode from the remote control
        No preprocessing
        You have to check that length > 0
            before handling the code value
        if the IR Receiver is not enabled, this will return -1
        '''
        if IR_RECEIVER_ENABLED:
            return ir_receiver.nextcode()
        else:
            print("Error with the Remote Controller")
            print("Please enable the IR Receiver in the Advanced Comms tool")
            return -1
##########################


class LineFollower(Sensor):
    '''
    The line follower detects the presence of a black line or its
      absence.
    You can use this in one of three ways.
    1. You can use read_position() to get a simple position status:
        center, left or right.
        these indicate the position of the black line.
        So if it says left, the GoPiGo has to turn right
    2. You can use read() to get a list of the five sensors.
        each position in the list will either be a 0 or a 1
        It is up to you to determine where the black line is.
    3. You can use read_raw_sensors() to get raw values from all sensors
        You will have to handle the calibration yourself
    4. the gpg argument is ignored. Needed for future compatibility
    '''

    def __init__(self, port="I2C", pinmode="",gpg=None):
        try:
            Sensor.__init__(self, port, "INPUT")
            self.set_descriptor("Line Follower")
            self.last_3_reads = []
            self.white_line = self.get_white_calibration()
            self.black_line = self.get_black_calibration()
            self.threshold = [w+((b-w)/2) for w,b in zip(self.white_line,self.black_line)]
        except:
            raise ValueError("Line Follower Library not found")

    def read_raw_sensors(self):
        '''
        Returns raw values from all sensors
        From 0 to 1023
        May return a list of -1 when there's a read error
        '''
        _grab_read()
        five_vals = line_sensor.read_sensor()
        _release_read()
        print ("raw values {}".format(five_vals))

        if five_vals != -1:
            return five_vals
        else:
            return [-1, -1, -1, -1, -1]

    def get_white_calibration(self):
        return line_sensor.get_white_line()

    def get_black_calibration(self):
        return line_sensor.get_black_line()

    def read(self):
        '''
        Returns a list of 5 values between 0 and 1
        Depends on the line sensor being calibrated first
            through the Line Sensor Calibration tool
        May return all -1 on a read error
        '''
        five_vals = [-1,-1,-1,-1,-1]


        five_vals = self.read_raw_sensors()

        line_result = []
        for sensor_reading,cur_threshold in zip(five_vals,self.threshold):
            if sensor_reading > cur_threshold:
                line_result.append(1)
            else:
                line_result.append(0)

        print ("Current read is {}".format(line_result))

        if five_vals != [-1,-1,-1,-1,-1]:
            print("appending")
            self.last_3_reads.append(line_result)
        if len(self.last_3_reads) > 3:
            self.last_3_reads.pop(0)

        print (self.last_3_reads)
        transpose = list(zip(*self.last_3_reads))
        avg_vals = []
        for sensor_reading in transpose:
            # print (sum(sensor_reading)//3)
            avg_vals.append(sum(sensor_reading)//3)

        print ("current avg: {}".format(avg_vals))
        return avg_vals

    def follow_line(self,fwd_speed=80):
        slight_turn_speed=int(.7*fwd_speed)
        while True:
            pos = self.read_position()
            print(pos)
            if pos == "Center":
                gopigo.forward()
            elif pos == "Left":
                gopigo.set_right_speed(0)
                gopigo.set_left_speed(slight_turn_speed)
            elif pos == "Right":
                gopigo.set_right_speed(slight_turn_speed)
                gopigo.set_left_speed(0)
            elif pos == "Black":
                gopigo.stop()
            elif pos == "White":
                gopigo.stop()

    def read_position(self):
        '''
        Returns a string telling where the black line is, compared to
            the GoPiGo
        Returns: "Left", "Right", "Center", "Black", "White"
        May return "Unknown"
        This method is not intelligent enough to handle intersections.
        '''
        five_vals = [-1,-1,-1,-1,-1]

        if _is_read_open():
            five_vals = self.read()

        if five_vals == [0, 0, 1, 0, 0] or five_vals == [0, 1, 1, 1, 0]:
            return "Center"
        if five_vals == [1, 1, 1, 1, 1]:
            return "Black"
        if five_vals == [0, 0, 0, 0, 0]:
            return "White"
        if five_vals == [0, 1, 1, 0, 0] or \
           five_vals == [0, 1, 0, 0, 0] or \
           five_vals == [1, 0, 0, 0, 0] or \
           five_vals == [1, 1, 0, 0, 0] or \
           five_vals == [1, 1, 1, 0, 0] or \
           five_vals == [1, 1, 1, 1, 0]:
            return "Left"
        if five_vals == [0, 0, 0, 1, 0] or \
           five_vals == [0, 0, 1, 1, 0] or \
           five_vals == [0, 0, 0, 0, 1] or \
           five_vals == [0, 0, 0, 1, 1] or \
           five_vals == [0, 0, 1, 1, 1] or \
           five_vals == [0, 1, 1, 1, 1]:
            return "Right"
        return "Unknown"

class DHTSensor(Sensor):

    def __init__(self, port="SERIAL",gpg=None):
        try:
     	    Sensor.__init__(self,port,"INPUT")
            self.filtered_temperature = [] # here we keep the temperature values after removing outliers
            self.filtered_humidity = [] # here we keep the filtered humidity values after removing the outliers

            self.lock = threading.Lock() # we are using locks so we don't have conflicts while accessing the shared variables
            self.event = threading.Event() # we are using an event so we can close the thread as soon as KeyboardInterrupt is raised

        except:
            raise ValueError("DHT Sensor not found")
    def read_temperature(self,sensor_type=0):
        _grab_read()
        temp=gopigo.dht(sensor_type)[0]
        _release_read()
        if temp == -2:
            return "Bad reading, trying again"
        elif temp == -3:
            return "Run the program as sudo"
        else:
            print("Temperature = %.02fC"%temp)
            return temp

    def read_humidity(self,sensor_type=0):
        _grab_read()
        humidity=gopigo.dht(sensor_type)[1]
        _release_read()
        if humidity == -2:
            return "Bad reading, trying again"
        elif humidity == -3:
            return "Run the program as sudo"
        else:
            print("Humidity = %.02f%%"%humidity)
            return humidity

    def read_dht(self,sensor_type=0):
        _grab_read()
        [temp , humidity]=gopigo.dht(sensor_type)
        _release_read()
        if temp ==-2.0 or humidity == -2.0:
            return "Bad reading, trying again"
        elif temp ==-3.0 or humidity == -3.0:
            return "Run the program as sudo"
        else:
            print("Temperature = %.02fC Humidity = %.02f%%"%(temp, humidity))
            return [temp, humidity] 
             
    # Derived from Robert's Code
    # function which eliminates the noise
    # by using a statistical model
    # we determine the standard normal deviation and we exclude anything that goes beyond a threshold
    # think of a probability distribution plot - we remove the extremes
    # the greater the std_factor, the more "forgiving" is the algorithm with the extreme values
    def eliminateNoise(self,values, std_factor = 2):
        mean = numpy.mean(values)
        standard_deviation = numpy.std(values)

        if standard_deviation == 0:
            return values

        final_values = [element for element in values if element > mean - std_factor * standard_deviation]
        final_values = [element for element in final_values if element < mean + std_factor * standard_deviation]

        return final_values
    # Derived from Robert's Code
    # function for processing the data
    # filtering, periods of time, yada yada
    def readingValues(self,sensor_type=0):
        seconds_window = 10 # after this many second we make a record
        values = []

        while not self.event.is_set():
            counter = 0
            while counter < seconds_window and not self.event.is_set():
                temp = None
                humidity = None
                try:
                    [temp, humidity] = gopigo.dht(sensor_type)

                except IOError:
                    print("we've got IO error")

                if math.isnan(temp) == False and math.isnan(humidity) == False:
                    values.append({"temp" : temp, "hum" : humidity})
                    counter += 1
                #else:
                    #print("we've got NaN")

                time.sleep(1)

            self.lock.acquire()
            self.filtered_temperature.append(numpy.mean(self.eliminateNoise([x["temp"] for x in values])))
            self.filtered_humidity.append(numpy.mean(self.eliminateNoise([x["hum"] for x in values])))
            self.lock.release()

            values = []
    
    # Derived from Robert's Code
    def continuous_read_dht(self):

        try:
            # here we start the thread
            # we use a thread in order to gather/process the data separately from the printing proceess
            data_collector = threading.Thread(target = self.readingValues)
            data_collector.start()

            while not self.event.is_set():
                if len(self.filtered_temperature) > 0: # or we could have used filtered_humidity instead
                    self.lock.acquire()

                    # here you can do whatever you want with the variables: print them, file them out, anything
                    temperature = self.filtered_temperature.pop()
                    humidity = self.filtered_humidity.pop()
                    print('{},Temperature:{:.01f}C, Humidity:{:.01f}%' .format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),temperature,humidity))

                    self.lock.release()

                # wait a second before the next check
                time.sleep(1)

            # wait until the thread is finished
            data_collector.join()
        except KeyboardInterrupt:
            self.event.set()

if __name__ == '__main__':
    import time
    b = Buzzer()
    print (b)
    print ("Sounding buzzer")
    b.sound_on()
    time.sleep(1)
    print ("buzzer off")
    b.sound_off()
    c=DHTSensor()
    c.read_humidity()
    c.read_temperature()
    c.read_dht()
    c.continuous_read_dht()
