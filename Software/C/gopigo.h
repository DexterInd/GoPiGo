// ####################################################################################                                                                  
// This library is used for communicating with the GoPiGo.                                
// http://www.dexterindustries.com/GoPiGo/                                                                
// History
// ------------------------------------------------
// Date              Comments
// 30 Aug 15          Initial Authoring
// 02 Feb 16          Support Encoders

// ## License
//
// GoPiGo for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
// Copyright (C) 2017  Dexter Industries

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.

// ####################################################################################

#ifndef GOPIGO_H
#define GOPIGO_H

#include <stdio.h>
#include <stdlib.h>
#include <linux/i2c-dev.h>
#include <fcntl.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <errno.h>
#include <stdbool.h>

extern int fd;
extern char *fileName;
extern int  address;
extern unsigned char w_buf[5],r_buf[32];
extern unsigned long reg_addr;

#define fwd_cmd              119        //Move forward with PID
#define motor_fwd_cmd        105        //Move forward without PID
#define bwd_cmd              115        //Move back with PID
#define motor_bwd_cmd        107        //Move back without PID
#define left_cmd             97            //Turn Left by turning off one motor
#define left_rot_cmd         98            //Rotate left by running both motors is opposite direction
#define right_cmd            100        //Turn Right by turning off one motor
#define right_rot_cmd        110        //Rotate Right by running both motors is opposite direction
#define stop_cmd             120        //Stop the GoPiGo
#define ispd_cmd             116        //Increase the speed by 10
#define dspd_cmd             103        //Decrease the speed by 10
#define m1_cmd               111         //Control motor1
#define m2_cmd               112         //Control motor2
#define read_motor_speed_cmd 114        //Get motor speed back

#define volt_cmd             118        //Read the voltage of the batteries
#define us_cmd               117        //Read the distance from the ultrasonic sensor
#define led_cmd              108        //Turn On/Off the LED's
#define servo_cmd            101        //Rotate the servo
#define enc_tgt_cmd          50            //Set the encoder targeting
#define fw_ver_cmd           20            //Read the firmware version
#define en_enc_cmd           51            //Enable the encoders
#define dis_enc_cmd          52            //Disable the encoders
#define read_enc_status_cmd  53            //Read encoder status
#define en_servo_cmd         61            //Enable the servo's    
#define dis_servo_cmd        60            //Disable the servo's
#define set_left_speed_cmd   70            //Set the speed of the right motor
#define set_right_speed_cmd  71            //Set the speed of the left motor
#define en_com_timeout_cmd   80            //Enable communication timeout
#define dis_com_timeout_cmd  81            //Disable communication timeout
#define timeout_status_cmd   82            //Read the timeout status
#define enc_read_cmd         53            //Read encoder values
#define trim_test_cmd        30            //Test the trim values
#define trim_write_cmd       31            //Write the trim values
#define trim_read_cmd        32        

#define digital_write_cmd    12          //Digital write on a port
#define digital_read_cmd     13          //Digital read on a port
#define analog_read_cmd      14          //Analog read on a port
#define analog_write_cmd     15          //Analog read on a port
#define pin_mode_cmd         16          //Set up the pin mode on a port

#define ir_read_cmd          21
#define ir_recv_pin_cmd      22
#define cpu_speed_cmd        25

//Initialize
int init(void);
//Write a register
int write_block(char cmd,char v1,char v2,char v3);
//Read 1 byte of data
char read_byte(void);
//Get voltage
float volt(void);

//Sleep in ms 
void pi_sleep(int t);

//Control Motor 1
int motor1(int direction,int speed);

//Control Motor 2
int motor2(int direction,int speed);

//Move the GoPiGo forward
int fwd(void);

//Move the GoPiGo forward without PID
int motor_fwd(void);

//Move GoPiGo back
int bwd(void);

//Move GoPiGo back without PID control
int motor_bwd(void);

//Turn GoPiGo Left slow (one motor off, better control)    
int left(void);

//Rotate GoPiGo left in same position (both motors moving in the opposite direction)
int left_rot(void);

//Turn GoPiGo right slow (one motor off, better control)
int right(void);

//Rotate GoPiGo right in same position both motors moving in the opposite direction)
int right_rot(void);

//Stop the GoPiGo
int stop(void);

//Increase the speed
int increase_speed(void);

//Decrease the speed
int decrease_speed(void);

//Trim test with the value specified
int trim_test(int value);

//Read the trim value in    EEPROM if present else return -3
int trim_read(void);

//Write the trim value to EEPROM, where -100=0 and 100=200
int trim_write(int value);

// Arduino Digital Read
int digitalRead(int pin);

// Arduino Digital Write
int digitalWrite(int pin, int value);

// Setting Up Pin mode on Arduino
int pinMode(int pin, char * mode);

// Read analog value from Pin
int analogRead(int pin);

// Write PWM
int analogWrite(int pin, int value);

//Read board revision
//    return:    voltage in V
int brd_rev(void);

//Read ultrasonic sensor
//    arg:
//        pin ->     Pin number on which the US sensor is connected
//    return:        distance in cm
int us_dist(int pin);

//Read motor speed (0-255)
//    arg:
//        speed -> pointer to array of 2 bytes [motor1, motor2], allocated before
void read_motor_speed(unsigned char* speed);

//Turn led on
//    arg:
//        l_id: 1 for left LED and 0 for right LED
int led_on(int l_id);

//Turn led off
//    arg:
//        l_id: 1 for left LED and 0 for right LED
int led_off(int l_id);

//Set servo position
//    arg:
//        position: angle in degrees to set the servo at
int servo(int position);

//Returns the firmware version
int fw_ver(void);

//Set speed of the left motor
//    arg:
//        speed-> 0-255
int set_left_speed(int speed);

//Set speed of the right motor
//    arg:
//        speed-> 0-255
int set_right_speed(int speed);

//Set speed of the both motors
//    arg:
//        speed-> 0-255
int set_speed(int speed);

//Read encoder value
//    arg:
//        motor ->     0 for motor1 and 1 for motor2
//    return:        distance in cm
int enc_read(int motor);

// Enable the encoders (enabled by default)
int enable_encoders(void);

// Disable the encoders (use this if you don't want to use the encoders)
int disable_encoders(void);

//Set encoder targeting on
//arg:
//    m1: 0 to disable targeting for m1, 1 to enable it
//    m2:    1 to disable targeting for m2, 1 to enable it
//    target: number of encoder pulses to target (18 per revolution)
int enc_tgt(int m1, int m2, int target);

//Read encoder status
//    return:    0 if encoder target is reached
int read_enc_status(void);

//Read timeout status
//    return:    0 if timeout is reached
int read_timeout_status(void);

#endif /*GOPIGO_H */
