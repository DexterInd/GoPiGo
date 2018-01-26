'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
This file attempts to create one of eac sensor and sets its mutex use to True.
As the use_mutex is a member of the base Sensor class, we check if the info is passed down properly
It does not test whether mutex is properly used inside each sensor
In fact some sensors will make no use of it at all
(on GPG3 some sensors do not require mutex)
Nicole Parrot
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

import easygopigo as easy

g = easy.EasyGoPiGo(use_mutex=True)

light_sensor = easy.LightSensor(gpg=g, use_mutex = True)
buzzer = easy.Buzzer(gpg=g, use_mutex = True)
led = easy.Led(gpg=g, use_mutex = True)
motion = easy.MotionSensor(gpg=g, use_mutex = True)
button = easy.ButtonSensor(gpg=g, use_mutex = True)
remote = easy.Remote(gpg=g, use_mutex = True)
line_follower = easy.LineFollower(gpg=g, use_mutex = True)
servo = easy.Servo(gpg=g, use_mutex = True)
distance_sensor = easy.DistanceSensor(gpg=g, use_mutex = True)
dht = easy.DHTSensor(gpg=g, use_mutex = True)
assert(g.use_mutex == True)
assert(light_sensor.use_mutex == True)
assert(buzzer.use_mutex == True)
assert(led.use_mutex == True)
assert(motion.use_mutex == True)
assert(button.use_mutex == True)
assert(remote.use_mutex == True)
assert(line_follower.use_mutex == True)
assert(servo.use_mutex == True)
assert(distance_sensor.use_mutex == True)
assert(dht.use_mutex == True)
print("Done")

