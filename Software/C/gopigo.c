// ####################################################################################                                                                  
// This library is used for communicating with the GoPiGo.                                
// http://www.dexterindustries.com/GoPiGo/                                                                
// History
// ------------------------------------------------
// Date      		Comments
// 30 Aug 15	  	Initial Authoring

// ## License
//
// GoPiGo for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
// Copyright (C) 2015  Dexter Industries

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
#include "gopigo.h"

int fd;													
char *fileName = "/dev/i2c-1";								
int  address = 0x08;									
unsigned char w_buf[5],r_buf[32];	
unsigned long reg_addr=0;    
int version=200;	//Initialized with invalid version
int v16_thresh=790;
int LED_L=1,LED_R=0;

int init(void)
{
	int i,raw;
	if ((fd = open(fileName, O_RDWR)) < 0) 
	{					// Open port for reading and writing
		printf("Failed to open i2c port\n");
		return -1;
	}
	
	if (ioctl(fd, I2C_SLAVE, address) < 0) 
	{					// Set the port options and set the address of the device 
		printf("Unable to get bus access to talk to slave\n");
		return -1;
	}
	for(i=0;i<10;i++)
		raw=analogRead(7);
	if(raw>v16_thresh)
		version=16;
	else
		version=14;
	return 1;
}
//Write a register
int write_block(char cmd,char v1,char v2,char v3)
{
    w_buf[0]=1;													
	w_buf[1]=cmd;
    w_buf[2]=v1;
    w_buf[3]=v2;
    w_buf[4]=v3;
    
    if ((write(fd, w_buf, 5)) != 5) 
    {								
        printf("Error writing to GoPiGo\n");
		usleep(10000);
        return -1;
    }
	usleep(10000);
    return 1; 
}

//Read 1 byte of data
char read_byte(void)
{
    int reg_size=1;
    
	if (read(fd, r_buf, reg_size) != reg_size) {
		usleep(10000);		
		printf("Unable to read from GoPiGo\n");
		exit(1);
        return -1;
	}
    usleep(10000);
    return r_buf[0];
}

float volt(void)
{
    int v[2];
    float voltage;
    write_block(volt_cmd,0,0,0);
    pi_sleep(100);
    v[0]=read_byte();
    v[1]=read_byte();
    voltage=v[0]*256+v[1];
	voltage=(5.0*voltage/1024)/.4;
    return voltage;
}

int fwd()
{
    return write_block(fwd_cmd,0,0,0);
}
int stop()
{
    return write_block(stop_cmd,0,0,0);
}

void pi_sleep(int t) 
{
	usleep(t*1000);
}

//Control Motor 1
int motor1(int direction,int speed)
{
	return write_block(m1_cmd,direction,speed,0);
}

//Control Motor 2
int motor2(int direction,int speed)
{
	return write_block(m2_cmd,direction,speed,0);
}

//Move the GoPiGo forward without PID
int motor_fwd(void)
{
	return write_block(motor_fwd_cmd,0,0,0);
}
//Move GoPiGo back
int bwd(void)
{
	return write_block(motor_bwd_cmd,0,0,0);
}

//Move GoPiGo back without PID control
int motor_bwd(void)
{
	return write_block(motor_bwd_cmd,0,0,0);
}

//Turn GoPiGo Left slow (one motor off, better control)	
int left(void)
{
	return write_block(left_cmd,0,0,0);
}

//Rotate GoPiGo left in same position (both motors moving in the opposite direction)
int left_rot(void)
{
	return write_block(left_rot_cmd,0,0,0);
}

//Turn GoPiGo right slow (one motor off, better control)
int right(void)
{
	return write_block(right_cmd,0,0,0);
}

//Rotate GoPiGo right in same position both motors moving in the opposite direction)
int right_rot(void)
{
	return write_block(right_rot_cmd,0,0,0);
}

//Increase the speed
int increase_speed(void)
{
	return write_block(ispd_cmd,0,0,0);
}

//Decrease the speed
int decrease_speed(void)
{
	return write_block(dspd_cmd,0,0,0);
}

//Trim test with the value specified
int trim_test(int value)
{
	if (value>100)
		value=100;
	else if(value<-100)
		value=-100;
	value+=100;
	return write_block(trim_test_cmd,value,0,0);
}

//Read the trim value in	EEPROM if present else return -3
int trim_read(void)
{
	int b1,b2,trim;
	if(write_block(trim_read_cmd,0,0,0)==-1)
		return -1;
	pi_sleep(80);
	b1=read_byte();
    b2=read_byte();
	if(b1==-1 || b2==-1)
		return -1;
	trim=b1*256+b2;
	if (trim ==255)
		return -3;
	return trim;
}

//Write the trim value to EEPROM, where -100=0 and 100=200
int trim_write(int value)
{
	if (value>100)
		value=100;
	else if(value<-100)
		value=-100;
	value+=100;
	return write_block(trim_write_cmd,0,0,0);
}

// Arduino Digital Read
int digitalRead(int pin)
{
	int dRead;
	if(pin==10||pin==15||pin==0||pin==1)
	{
		if(write_block(digital_read_cmd,pin,0,0)==-1)
			return -1;
		pi_sleep(100);
		dRead=read_byte();
		read_byte();
		if(dRead==-1)
			return -1;
		return dRead;
	}
	else
		return -2;
}
// Arduino Digital Write
int digitalWrite(int pin, int value)
{
	if(value==0 || value==1)
		return write_block(digital_write_cmd,pin,value,0);
	else
		return -2;
}

// Setting Up Pin mode on Arduino
int pinMode(int pin, char * mode)
{
	if(strcmp(mode,"ÏNPUT")==0)
		return write_block(pin_mode_cmd,pin,0,0);
	else if(strcmp(mode,"OUTPUT")==0)
		return write_block(pin_mode_cmd,pin,1,0);
	return -1;
}

// Read analog value from Pin
int analogRead(int pin)
{
	int b1,b2;
	write_block(analog_read_cmd,pin,0,0);
	pi_sleep(70);
	b1=read_byte();
	b2=read_byte();
	if(b1==-1 || b2==-1)
		return -1;
	return b1* 256 + b2;
}

// Write PWM
int analogWrite(int pin, int value)
{
	if(pin==10)
	{
		write_block(analog_write_cmd,pin,value,0);
		return 1;
	}
	return -2;
}

//Read board hardware revision
int brd_rev(void)
{
	return version;
}
//Read ultrasonic sensor
//	arg:
//		pin -> 	Pin number on which the US sensor is connected
//	return:		distance in cm
int us_dist(int pin)
{
	int b1,b2;
	write_block(us_cmd,pin,0,0);
	pi_sleep(80);
	b1=read_byte();
	b2=read_byte();
	if(b1==-1 || b2==-1)
		return -1;
	return b1* 256 + b2;
}
//Turn led on
//	arg:
//		l_id: 1 for left LED and 0 for right LED
int led_on(int l_id)
{
	int r_led,l_led;
	if (version>14)
	{
		r_led=16;
		l_led=17;
	}
	else
	{
		r_led=5;
		l_led=10;
	}
	
	if(l_id==LED_L || l_id==LED_R)
	{
		if(l_id==LED_L)
		{ 
			pinMode(l_led,"OUTPUT");
			digitalWrite(l_led,1);
		}
		else if(l_id==LED_R)
		{
			pinMode(r_led,"OUTPUT");
			digitalWrite(r_led,1);
		}
		return 1;
	}
	else
		return -1;
}
//Turn led off
//	arg:
//		l_id: 1 for left LED and 0 for right LED
int led_off(int l_id)
{
	int r_led,l_led;
	if (version>14)
	{
		r_led=16;
		l_led=17;
	}
	else
	{
		r_led=5;
		l_led=10;
	}
	
	if(l_id==LED_L || l_id==LED_R)
	{
		if(l_id==LED_L)
		{
			pinMode(l_led,"OUTPUT");
			digitalWrite(l_led,0);
		}
		else if(l_id==LED_R)
		{
			pinMode(r_led,"OUTPUT");
			digitalWrite(r_led,0);
		}
		return 1;
	}
	else
		return -1;
}
//Set servo position
//	arg:
//		position: angle in degrees to set the servo at
int servo(int position)
{
	return write_block(servo_cmd,position,0,0);
}

//Returns the firmware version
int fw_ver(void)
{
	int ver;
	write_block(fw_ver_cmd,0,0,0);
	pi_sleep(100);
	ver=read_byte();
	read_byte();
	if(ver==-1)
		return -1;
	return ver;
}
//Set speed of the left motor
//	arg:
//		speed-> 0-255
int set_left_speed(int speed)
{
	if(speed >255)
		speed =255;
	else if(speed <0)
		speed =0;
	return write_block(set_left_speed_cmd,speed,0,0);
}
//Set speed of the right motor
//	arg:
//		speed-> 0-255
int set_right_speed(int speed)
{
	if(speed >255)
		speed =255;
	else if(speed <0)
		speed =0;
	return write_block(set_right_speed_cmd,speed,0,0);
}
//Set speed of the both motors
//	arg:
//		speed-> 0-255
int set_speed(int speed)
{
	if(speed >255)
		speed =255;
	else if(speed <0)
		speed =0;
	set_left_speed(speed);
	pi_sleep(100);
	set_right_speed(speed);
	return 1;
}