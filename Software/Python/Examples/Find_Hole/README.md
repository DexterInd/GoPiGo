#Find Hole Example

This example will search for a "hole" for the [GoPiGo](http://www.dexterindustries.com/shop/gopigo-starter-kit-2/) to roll through.  It will stop if it does not find a suitable hole in the objects around it to go through.  The example uses the [GoPiGo Servo](http://www.dexterindustries.com/shop/servo-package/) and [GoPiGo Ultrasonic](http://www.dexterindustries.com/shop/ultrasonic-sensor/) sensor to find the holes.

The goal of this example is to allow the GoPiGo to:

1. Move forward until it is within 20cm of an obstacle
2. Stop and scan the immediate area to find a hole large enough for the chassis to fit
3. Turn toward the hole.
4. Move forward through the hole.
5. Repeat

## Note that if the robot can not find a hole in the 100 degree code in front of it, it will stop.  
