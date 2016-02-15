#!/usr/bin/env python

# ! Attach Ultrasonic sensor to A1 Port.
# ! Make sound from the buzzer connected to the D11 port by giving the power value
# Camera attached.

'''
    * On startup, the ultrasonic sensor is armed. 
    * When the us sensor detects a distance it starts:
        - Beeps
        - Lights blink
        - Plays yells sound
        - Takes pictures every second.
'''

from gopigo import *
import sys
import time
import pygame
import atexit
import picamera

atexit.register(stop)

'''
Load up default values, and blink front LEDS twice to show readiness
'''

pygame.mixer.init()
pygame.mixer.music.load("yells.mp3")
camera = picamera.PiCamera()

buzz_pin = 10
onoff = 0
distance_to_stop = 10
count = 0

i=0
for i in range(2):
    led_on(0)
    led_on(1)
    time.sleep(0.5)
    led_off(0)
    led_off(1)
    time.sleep(0.5)


while True:
    count = count + 1
    # Toggle onoff
    if onoff == 0:
        onoff = 1
    else:
        onoff = 0

    # Read Ultrasonic Sensor.
    dist=us_dist(15)            #Find the distance of the object in front
    print "Dist:",dist,'cm'
    if dist<distance_to_stop:   #If the object is closer than the "distance_to_stop" distance, stop the GoPiGo
        print "Stopping"
        stop()                  #Stop the GoPiGo
        led_off(0)              # Turn off LEDs
        led_off(1)              # Turn off LEDs
        analogWrite(buzz_pin,0)     # Turn off Buzzer.
        pygame.mixer.music.pause() # Turn off yells

    else:
        fwd()                         # start attacking by going forward
        pygame.mixer.music.play()     # start yelling
        # Flash LEDs, toggle Buzzer
        if onoff:
            print "LED ON"
            led_on(0)
            led_off(1)
            analogWrite(buzz_pin,255)
        else:
            print "LED OFF"
            led_on(1)
            led_off(0)
            analogWrite(buzz_pin,0)

        # capture an image of the culprit
        image_count = "/home/pi/Desktop/image_" + str(count) + ".jpg"
        camera.capture(image_count)
    
    time.sleep(0.5)
