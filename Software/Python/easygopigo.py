#!/usr/bin/env python
# from __future__ import print_function
# from __future__ import division
# from builtins import input

import sys
# import tty
# import select
import time

try:
    import gopigo
except:
    pass
# import os

# the following libraries may or may not be installed
# nor needed
from I2C_mutex import Mutex

mutex = Mutex()

def _ifMutexAcquire(mutex_enabled = False):
    """
    Acquires the I2C if the ``use_mutex`` parameter of the constructor was set to ``True``.
    Always acquires if system-wide mutex has been set.
    
    """
    if mutex_enabled or mutex.overall_mutex()==True:
        mutex.acquire()

def _ifMutexRelease(mutex_enabled = False):
    """
    Releases the I2C if the ``use_mutex`` parameter of the constructor was set to ``True``.
    """
    if mutex_enabled or mutex.overall_mutex()==True:
        mutex.release()

try:
    from line_follower import line_sensor
    from line_follower import scratch_line
    is_line_follower_accessible = True
except:
    is_line_follower_accessible = False

##########################

def debug(in_str):
    if False:
        print(in_str)


class EasyGoPiGo():
    '''
    Wrapper to access the gopigo functionality with mutex in place
    this makes the gopigo thread safe and process safe
    if mutex is not available, then it's just a direct access to gopigo
    '''
    def __init__(self, use_mutex = False):
        '''
        On Init, set speed to half-way, so GoPiGo is predictable
            and not too fast.
        '''

        self.DEFAULT_SPEED = 128
        gopigo.set_speed(self.DEFAULT_SPEED)
        self.use_mutex = use_mutex

    def volt(self):
        _ifMutexAcquire(self.use_mutex)
        try:
            voltage = gopigo.volt()
        except:
            voltage = 0
        _ifMutexRelease(self.use_mutex)
        return voltage

    def stop(self):
        # no locking is required here
        try:
            gopigo.stop()
        except:
            pass

    def forward(self):
        _ifMutexAcquire(self.use_mutex)
        try:
            val = gopigo.forward()
        except Exception as e:
            print("easygopigo fwd: {}".format(e))
            pass
        _ifMutexRelease(self.use_mutex)

    def backward(self):
        _ifMutexAcquire(self.use_mutex)
        try:
            val = gopigo.backward()
        except Exception as e:
            print("easygopigo bwd: {}".format(e))
            pass
        finally:
            _ifMutexRelease(self.use_mutex)


    def left(self):
        _ifMutexAcquire(self.use_mutex)
        try:
            gopigo.left()
        except:
            pass
        finally:
            _ifMutexRelease(self.use_mutex)


    def right(self):
        _ifMutexAcquire(self.use_mutex)
        try:
            gopigo.right()
        except:
            pass
        _ifMutexRelease(self.use_mutex)

    def set_speed(self,new_speed):
        _ifMutexAcquire(self.use_mutex)
        try:
            gopigo.set_speed(new_speed)
        except:
            pass
        finally:
            _ifMutexRelease(self.use_mutex)

    def reset_speed(self):
        _ifMutexAcquire(self.use_mutex)
        try:
            gopigo.set_speed(self.DEFAULT_SPEED)
        except:
            pass
        finally:
            _ifMutexRelease(self.use_mutex)

    def set_left_speed(self,new_speed):
        _ifMutexAcquire(self.use_mutex)
        try:
            gopigo.set_left_speed(new_speed)
        except:
            pass
        _ifMutexRelease(self.use_mutex)

    def set_right_speed(self,new_speed):
        _ifMutexAcquire(self.use_mutex)
        try:
            gopigo.set_right_speed(new_speed)
        except:
            pass
        finally:
            _ifMutexRelease(self.use_mutex)

    def led_on(self,led_id):
        _ifMutexAcquire(self.use_mutex)
        try:
            gopigo.led_on(led_id)
        except:
            pass
        finally:
            _ifMutexRelease(self.use_mutex)

    def led_off(self,led_id):
        _ifMutexAcquire(self.use_mutex)
        try:
            gopigo.led_off(led_id)
        except:
            pass
        finally:
            _ifMutexRelease(self.use_mutex)

    def trim_read(self):
        _ifMutexAcquire(self.use_mutex)
        try:
            current_trim = int(gopigo.trim_read())
        except:
            pass
        _ifMutexRelease(self.use_mutex)
        return current_trim

    def trim_write(self,set_trim_to):
        _ifMutexAcquire(self.use_mutex)
        try:
            gopigo.trim_write(int(set_trim_to))
        except:
            pass
        _ifMutexRelease(self.use_mutex)

    def init_light_sensor(self, port="A1"):
        return LightSensor(port, gpg=self, use_mutex=self.use_mutex)

    def init_sound_sensor(self, port="A1"):
        return SoundSensor(port, gpg=self, use_mutex=self.use_mutex)

    def init_loudness_sensor(self, port="AD1"):
        return LoudnessSensor(port, gpg=self, use_mutex=self.use_mutex)

    def init_ultrasonic_sensor(self, port="A1"):
        return UltraSonicSensor(port, gpg=self, use_mutex=self.use_mutex)

    def init_buzzer(self, port="D11"):
        return Buzzer(port, gpg=self, use_mutex=self.use_mutex)

    def init_led(self, port="D11"):
        return Led(port, gpg=self, use_mutex=self.use_mutex)

    def init_button_sensor(self, port="D11"):
        return ButtonSensor(port, gpg=self, use_mutex=self.use_mutex)

    def init_line_follower(self, port="I2C"):
        return LineFollower(port, gpg=self, use_mutex=self.use_mutex )

    def init_servo(self, port="SERVO"):
        return Servo(port, gpg=self, use_mutex=self.use_mutex)

    def init_distance_sensor(self, port="I2C"):
        try:
            from di_sensors import easy_distance_sensor
            return DistanceSensor(port, gpg=self, use_mutex=self.use_mutex)
        except:
            print("DI Sensor library not found")
            return None
        
    def init_dht_sensor(self, port="SERIAL", sensor_type = 0):
        return DHTSensor(port, self, sensor_type, use_mutex=self.use_mutex)

    def init_remote(self, port="SERIAL"):
        return Remote(port="SERIAL", gpg=self, use_mutex=self.use_mutex)

    def init_motion_sensor(self, port="D11"):
        return MotionSensor(port, gpg=self, use_mutex=self.use_mutex)



#############################################################
# the following is in a try/except structure because it depends
# on the date of gopigo.py
#############################################################
try:
    PORTS = {"A1": gopigo.analogPort, "D11": gopigo.digitalPort,
             "SERIAL": -1, "I2C": -2, "SERVO": -3}
except:
    PORTS = {"A1": 15, "D11": 10, "SERIAL": -1, "I2C": -2, "SERVO": -3}


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
    def __init__(self, port, pinmode, use_mutex=False):
        '''
        port = one of PORTS keys
        pinmode = "INPUT", "OUTPUT", "SERIAL" (which gets ignored), "SERVO"
        '''
        debug("Sensor init")
        debug(pinmode)
        self.setPort(port)
        self.setPinMode(pinmode)
        self.use_mutex = use_mutex
        if pinmode == "INPUT" or pinmode == "OUTPUT":
            try:
                gopigo.pinMode(self.getPortID(), self.getPinMode())
            except:
                pass

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

    def reconfig_bus(self):
        '''
        Does nothing. Placeholder for compatibility with GoPiGo3
        '''
        pass
##########################


class DigitalSensor(Sensor):
    '''
    Implements read and write methods
    '''
    def __init__(self, port, pinmode, use_mutex = False):
        debug("DigitalSensor init")
        self.pin = DIGITAL
        Sensor.__init__(self, port, pinmode, use_mutex)


    def read(self):
        '''
        tries to get a value up to 10 times.
        As soon as a valid value is read, it returns either 0 or 1
        returns -1 after 10 unsuccessful tries
        '''
        okay = False
        error_count = 0

        while not okay and error_count < 10:
            _ifMutexAcquire(self.use_mutex)
            try:
                rtn = int(gopigo.digitalRead(self.getPortID()))
                okay = True
            except:
                error_count += 1
            finally:
                _ifMutexRelease(self.use_mutex)

        if error_count > 10:
            return -1
        else:
            return rtn

    def write(self, power):
        self.value = power

        _ifMutexAcquire(self.use_mutex)
        try:
            return_value = gopigo.digitalWrite(self.getPortID(), power)
        except:
            pass
        finally:
            _ifMutexRelease(self.use_mutex)

        return return_value
##########################


class AnalogSensor(Sensor):
    '''
    implements read and write methods
    '''
    def __init__(self, port, pinmode, use_mutex = False):
        debug("AnalogSensor init")
        self.value = 0
        self.pin = ANALOG
        self._max_value = 1024
        Sensor.__init__(self, port, pinmode, use_mutex)

    def read(self):
        _ifMutexAcquire(self.use_mutex)
        try:
            self.value = gopigo.analogRead(self.getPortID())
        except:
            pass
        finally:
            _ifMutexRelease(self.use_mutex)

        return self.value

    def percent_read(self):
        value = int(self.read()) * 100 // self._max_value
        # Some sensors - like the loudness_sensor -
        # can actually return higher than 100% so let's clip it
        # and keep classrooms within an acceptable noise level
        if value > 100:
            value = 100
        # print(value)
        return value

    def write(self, power):
        self.value = power
        _ifMutexAcquire(self.use_mutex)
        try:
            return_value = gopigo.analogWrite(self.getPortID(), power)
        except:
            pass
        finally:
            _ifMutexRelease(self.use_mutex)
        return return_value
##########################


class LightSensor(AnalogSensor):
    """
    Creates a light sensor from which we can read.
    Light sensor is by default on pin A1(A-one)
    self.pin takes a value of 0 when on analog pin (default value)
        takes a value of 1 when on digital pin
    """
    def __init__(self, port="A1", gpg = None, use_mutex = False):
        debug("LightSensor init")
        AnalogSensor.__init__(self, port, "INPUT", use_mutex)
        self.set_descriptor("Light sensor")
##########################


class SoundSensor(AnalogSensor):
    """
    Creates a sound sensor
    """
    def __init__(self, port="A1", gpg = None, use_mutex = False):
        debug("Sound Sensor on port "+port)
        AnalogSensor.__init__(self, port, "INPUT", use_mutex)
        self.set_descriptor("Sound sensor")
##########################


class LoudnessSensor(AnalogSensor):
    """
    Creates a Loudness sensor
    """
    def __init__(self, port="A1", gpg = None, use_mutex = False):
        debug("Loudness Sensor on port "+port)
        AnalogSensor.__init__(self, port, "INPUT", use_mutex)
        self.set_descriptor("Loudness sensor")
        self._max_value = 100
##########################


class UltraSonicSensor(AnalogSensor):

    def __init__(self, port="A1", gpg=None, use_mutex = False):
        debug("Ultrasonic Sensor on port "+port)
        AnalogSensor.__init__(self, port, "INPUT", use_mutex)
        self.safe_distance = 300
        self.set_descriptor("Ultrasonic sensor")
        self.port = port

    def is_too_close(self):
        too_close = False
        _ifMutexAcquire(self.use_mutex)
        try:
            if gopigo.us_dist(PORTS[self.port]) < self.get_safe_distance():
                too_close = True
        except:
            pass
        finally:
            _ifMutexRelease(self.use_mutex)
        return too_close

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
            _ifMutexAcquire(self.use_mutex)
            try:
                value = gopigo.corrected_us_dist(PORTS[self.port])
            except Exception as e:
                print("UltraSonicSensor read(): {}".format(e))
                pass
            finally:
                _ifMutexRelease(self.use_mutex)

            if value < 300 and value > 0:
                readings.append(value)
            else:
                skip +=1
                if skip > 5:
                    break
            time.sleep(0.05)

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
    def __init__(self, port="D11", gpg=None, use_mutex = False):
        AnalogSensor.__init__(self, port, "OUTPUT", use_mutex)
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
    def __init__(self, port = "D11", gpg = None, use_mutex = False):
        AnalogSensor.__init__(self, port, "OUTPUT", use_mutex)
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
    def __init__(self, port = "D11", gpg = None, use_mutex = False):
        DigitalSensor.__init__(self, port, "INPUT", use_mutex)
        self.set_descriptor("Motion Sensor")
##########################


class ButtonSensor(DigitalSensor):

    def __init__(self, port = "D11", gpg = None, use_mutex = False):
        DigitalSensor.__init__(self, port, "INPUT", use_mutex)
        self.set_descriptor("Button sensor")

    def is_button_pressed(self):
        return self.read() == 1
##########################


class Remote(Sensor):

    def __init__(self, port = "SERIAL", gpg = None, use_mutex = False):
        global IR_RECEIVER_ENABLED
        # IR Receiver
        try:
            import ir_receiver
            IR_RECEIVER_ENABLED = True
        except:
            IR_RECEIVER_ENABLED = False
            raise ImportError("IR sensor not enabled")

        if IR_RECEIVER_ENABLED:
            Sensor.__init__(self, port, "SERIAL", use_mutex)
            self.set_descriptor("Remote Control")

    def is_enabled(self):
        return IR_RECEIVER_ENABLED

    def get_remote_code(self):
        '''
        Returns the keycode from the remote control
        No preprocessing
        You have to check that length > 0
            before handling the code value
        '''

        if IR_RECEIVER_ENABLED:
            import ir_receiver
            key = ir_receiver.nextcode(consume=False)
        else:
            key = ""
        try:
            # in python3, key will come in as a byte
            key = key.decode("utf-8") 
        except AttributeError:
            # in python2, key will be a string, so no need to do anything
            pass

        return key

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

    def __init__(self,
                port = "I2C",
                pinmode = "",
                gpg = None,
                use_mutex = False):
        try:
            Sensor.__init__(self, port, "INPUT", use_mutex)
            self.set_descriptor("Line Follower")
            self.last_3_reads = []
            self.white_line = self.get_white_calibration()
            self.black_line = self.get_black_calibration()
            self.threshold = [w+((b-w)/2) for w,b in zip(self.white_line,self.black_line)]
        except:
            raise ValueError("Line Follower Library not found")

        # Needed for Bloxter
        try:
            from di_sensors import easy_line_follower
            self._lf = easy_line_follower.EasyLineFollower(port=port)
        except:
            self._lf = None

        self.use_mutex = use_mutex

    def read_raw_sensors(self):
        '''
        Returns raw values from all sensors
        From 0 to 1023
        May return a list of -1 when there's a read error
        '''

        _ifMutexAcquire(self.use_mutex)
        try:
            five_vals = line_sensor.read_sensor()
        except:
            pass
        finally:
            _ifMutexRelease(self.use_mutex)
        debug ("raw values {}".format(five_vals))

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

        debug ("Current read is {}".format(line_result))

        if five_vals != [-1,-1,-1,-1,-1]:
            debug("appending")
            self.last_3_reads.append(line_result)
        if len(self.last_3_reads) > 3:
            self.last_3_reads.pop(0)

        debug (self.last_3_reads)
        transpose = list(zip(*self.last_3_reads))
        avg_vals = []
        for sensor_reading in transpose:
            # print (sum(sensor_reading)//3)
            avg_vals.append(sum(sensor_reading)//3)

        debug ("current avg: {}".format(avg_vals))
        return avg_vals

    def follow_line(self, fwd_speed = 80):
        slight_turn_speed=int(.7*fwd_speed)
        while True:
            pos = self.read_position()
            debug(pos)
            if pos == "center":
                gopigo.forward()
            elif pos == "left":
                gopigo.set_right_speed(0)
                gopigo.set_left_speed(slight_turn_speed)
            elif pos == "right":
                gopigo.set_right_speed(slight_turn_speed)
                gopigo.set_left_speed(0)
            elif pos == "black":
                gopigo.stop()
            elif pos == "white":
                gopigo.stop()

    def read_position(self):
        '''
        Returns a string telling where the black line is, compared to
            the GoPiGo
        Returns: "Left", "Right", "Center", "Black", "White"
        May return "Unknown"
        This method is not intelligent enough to handle intersections.
        '''
        five_vals = self.read()

        if five_vals == [0, 0, 1, 0, 0] or five_vals == [0, 1, 1, 1, 0]:
            return "center"
        if five_vals == [1, 1, 1, 1, 1]:
            return "black"
        if five_vals == [0, 0, 0, 0, 0]:
            return "white"
        if five_vals == [0, 1, 1, 0, 0] or \
           five_vals == [0, 1, 0, 0, 0] or \
           five_vals == [1, 0, 0, 0, 0] or \
           five_vals == [1, 1, 0, 0, 0] or \
           five_vals == [1, 1, 1, 0, 0] or \
           five_vals == [1, 1, 1, 1, 0]:
            return "left"
        if five_vals == [0, 0, 0, 1, 0] or \
           five_vals == [0, 0, 1, 1, 0] or \
           five_vals == [0, 0, 0, 0, 1] or \
           five_vals == [0, 0, 0, 1, 1] or \
           five_vals == [0, 0, 1, 1, 1] or \
           five_vals == [0, 1, 1, 1, 1]:
            return "right"
        return "unknown"

    def read_position_str(self):
        """
        returns a string of five letters indicating what the line sensor is seeing.
        'b' indicates that specific sensor has detected a black line.
        'w' indicates that specific sensor has not detected a black line.

        :returns: String indicating what the line follower just read.
        :rtype: str

        Here's an example of what could get returned:
            * ``'bbbbb'`` - when the line follower reads black on all sensors.
            * ``'wwbww'`` - when the line follower is perfectly centered.
            * ``'bbbww'`` - when the line follower reaches an intersection.
        """
        five_vals  = self.read()
        out_str = "".join(["b" if sensor_val == 1 else "w" for sensor_val in five_vals])
        return out_str

# Bloxter Support
    def position_bw(self):
        """
        This method is only here to support Bloxter and 
        fake di_sensors.easy_line_follower
        """
        try:
            return self._lf.position_bw()
        except ValueError as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            return -1

    def position_01(self):
        """
        This method is only here to support Bloxter and 
        fake di_sensors.easy_line_follower
        """
        try:
            return self._lf.position_01()
        except:
            return -1

    def position(self):
        """
        This method is only here to support Bloxter and 
        fake di_sensors.easy_line_follower
        """
        try:
            return self._lf.position()
        except:
            return -1

    def set_calibration(self, color):
        """
        This method is only here to support Bloxter and 
        fake di_sensors.easy_line_follower
        """
        try:
            return self._lf.set_calibration(color)
        except ValueError as e:
            print(e)
        except Exception as e:
            print(e)
            line_val = []

    def get_calibration(self, color):
        """
        This method is only here to support Bloxter and 
        fake di_sensors.easy_line_follower
        """
        try:
            return self._lf.get_calibration(color)
        except ValueError as e:
            print(e)
        except Exception as e:
            print(e)
            line_val = [] 

#######################################################################
#
# SERVO
#
#######################################################################

class Servo(Sensor):


    def __init__(self, port="SERVO", gpg=None, use_mutex = False):
        Sensor.__init__(self, port, "SERVO", use_mutex)
        gopigo.enable_servo()
        self.set_descriptor("Servo Motor")

    def rotate_servo(self, servo_position):
        if servo_position > 180:
            servo_position = 180
        if servo_position < 0:
            servo_position = 0
        gopigo.servo(servo_position)


#######################################################################
#
# DistanceSensor
#
#######################################################################
try:
    from di_sensors import distance_sensor

    class DistanceSensor(Sensor, distance_sensor.DistanceSensor):
        '''
        Wrapper to measure the distance in cms from the DI distance sensor.
        Connect the distance sensor to I2C port.
        '''
        def __init__(self, port="I2C", gpg=None, use_mutex = False):
            self.use_mutex = use_mutex

            try:
                Sensor.__init__(self, port, "INPUT", use_mutex)

                _ifMutexAcquire(self.use_mutex)
                try:
                    distance_sensor.DistanceSensor.__init__(self)
                except:
                    pass
                finally:
                    _ifMutexRelease(self.use_mutex)
                self.set_descriptor("Distance Sensor")
            except Exception as e:
                print(e)
                raise ValueError("Distance Sensor not found")

        # Returns the values in mm
        readings = []
        def read_mm(self):

            # 8190 is what the sensor sends when it's out of range
            # we're just setting a default value
            mm = 8190
            readings = []
            attempt = 0

            # try 3 times to have a reading that is
            # smaller than 8m or bigger than 5 mm.
            # if sensor insists on that value, then pass it on
            while (mm > 8000 or mm < 5) and attempt < 3:
                _ifMutexAcquire(self.use_mutex)
                try:
                    mm = self.read_range_single()
                except:
                    mm = 0
                _ifMutexRelease(self.use_mutex)
                attempt = attempt + 1
                time.sleep(0.001)

            # add the reading to our last 3 readings
            # a 0 value is possible when sensor is not found
            if (mm < 8000 and mm > 5) or mm == 0:
                readings.append(mm)
            if len(readings) > 3:
                readings.pop(0)

            # calculate an average and limit it to 5 > X > 3000
            if len(readings) > 1: # avoid division by 0
                mm = round(sum(readings) / float(len(readings)))
            if mm > 3000:
                mm = 3000

            return mm

        def read(self):
            cm = self.read_mm()//10
            return (cm)

        def read_inches(self):
            cm = self.read()
            return cm / 2.54

except:
    print("Distance Sensor likely not installed")
    pass

#######################################################################
#
# GROVE DHT Sensor
#
#######################################################################

class DHTSensor(Sensor):
    '''
    Support for the Adafruit DHT sensor, blue or white
    All imports are done internally so it's done on a as needed basis only
        as in many cases the DHT sensor is not connected.
    '''
    def __init__(self,
                    port="SERIAL",
                    gpg=None,
                    sensor_type=0,
                    use_mutex=False):
        try:
            Sensor.__init__(self, port, "INPUT", use_mutex)
        except:
            raise

        self.use_mutex = use_mutex

        try:
            self.sensor_type = sensor_type

            if self.sensor_type == 0:
                self.set_descriptor("Blue DHT Sensor")
            else:
                self.set_descriptor("White DHT Sensor")

        except Exception as e:
            print("DHTSensor: {}".format(e))
            raise ValueError("DHT Sensor not found")

    def read_temperature(self):
        '''
        Return values may be a float, or error strings
        TBD: raise errors instead of returning strings
        import done internally so it's done on a as needed basis only
        '''

        from di_sensors import DHT

        _ifMutexAcquire(self.use_mutex)
        temp = DHT.dht(self.sensor_type)[0]
        _ifMutexRelease(self.use_mutex)

        if temp == -2:
            return "Bad reading, trying again"
        elif temp == -3:
            return "Run the program as sudo"
        else:
            # print("Temperature = %.02fC"%temp)
            return temp

    def read_humidity(self):
        '''
        Return values may be a float, or error strings
        TBD: raise errors instead of returning strins
        '''
        from di_sensors import DHT

        _ifMutexAcquire(self.use_mutex)
        humidity = DHT.dht(self.sensor_type)[1]
        _ifMutexRelease(self.use_mutex)

        if humidity == -2:
            return "Bad reading, trying again"
        elif humidity == -3:
            return "Run the program as sudo"
        else:
            # print("Humidity = %.02f%%"%humidity)
            return humidity

    def read(self):
        from di_sensors import DHT

        _ifMutexAcquire(self.use_mutex)
        [temp , humidity]=DHT.dht(self.sensor_type)
        _ifMutexRelease(self.use_mutex)

        if temp ==-2.0 or humidity == -2.0:
            return "Bad reading, trying again"
        elif temp ==-3.0 or humidity == -3.0:
            return "Run the program as sudo"
        else:
            print("Temperature = %.02fC Humidity = %.02f%%"%(temp, humidity))
            return [temp, humidity]

#######################################################################


if __name__ == '__main__':
    import time
    b = Buzzer()
    print (b)
    print ("Sounding buzzer")
    b.sound_on()
    time.sleep(1)
    print ("buzzer off")
    b.sound_off()
