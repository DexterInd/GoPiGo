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


//Write a register
long write_block(char cmd,char v1,char v2,char v3)
{
    w_buf[0]=1;													
	w_buf[1]=cmd;
    w_buf[2]=v1;
    w_buf[3]=v2;
    w_buf[4]=v3;
    
    if ((write(fd, w_buf, 5)) != 5) 
    {								
        printf("Error writing to i2c slave\n");
        return -1;
    }
    return 1; 
}

//Read 1 byte of data
char read_byte(void)
{
    int reg_size=1;
    
	if (read(fd, r_buf, reg_size) != reg_size) {								
		printf("Unable to read from slave\n");
		exit(1);
        return -1;
	}
    
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

int pi_sleep(int t)
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
	trim=b1*256+b1;
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
		return write_block(digital_write_cmd,pin,0,0);
	else
		return -2;
}