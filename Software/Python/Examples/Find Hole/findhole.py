#!/usr/bin/python
'''
This is inspired by both the Ultrasonic Basic Obstacle Avoider 
and Ultrasonic_Servo examples. 

Essentially, the gopigo should: 
  - Move fwd until it is within 20cm of an obstacle
  - Stop
  - Scan the room
  - Find a space between obstacles big enough to fit
  - Turn in that direction
  - Move fwd until it is within 20cm of an obstacle
  - Etc.
'''

from gopigo import *
import math

# Should move to gopigo.py
CHASS_WID = 13.5 # Chassis is ~13.5 cm wide.

distance_to_stop=20

def main():
    move(distance_to_stop)
    readings = scan_room()
    #findhole
    #verify
    #turn
    #repeat

def move(min_dist):
    fwd()
    while True:
        dist=us_dist(15)
        if dist<min_dist:
            stop()
            break
        time.sleep(.1)
    return

def scan_room():
    '''
    Start at 0 and move to 180 in increments.
    Angle required to fit chass @20cm away is:
        degrees(atan(CHASS_WID/20))
    Increments angles should be 1/2 of that.
    Looking for 3 consecutive readings of inf.
    3 misses won't guarantee a big enough hole
     because not every obstacle will be 20cm away,
     but it is a good place to start, and more
     importantly, gives us edges to use to 
     measure.
    
    Return list of angle,dist.
    '''

def calc_xy(meas):
    '''
    Given an angle and distance, return (x,y) tuple.
    x = dist*cos(radians(angle))
    y = dist*sin(radians(angle))
    '''

def calc_gap(xy1,xy2):
    '''
    Given two points represented by (x,y) tuples, 
    calculate the distance between the two points.
    dist is the hyp of the triangle.
    
    dist = sqrt((x1-x2)^2 + (y1-y2)^2)
    '''  
