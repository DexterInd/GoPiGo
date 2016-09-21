// ####################################################################################
// Dexter Industries line sensor C library
//
//This library provides the basic functions to access the sensor data from the line sensor
//http://www.dexterindustries.com/GoPiGo/gopigo-line-follower-getting-started/
//
// History
// ------------------------------------------------
// Shoban Narayan
// Date               Comments
// 21 Sep 16          Initial Authoring

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


#include "line_sensor.h"
 
int fd;
char *fileName = "/dev/i2c-1";
unsigned char w_buf[WRITE_BUF_SIZE],r_buf[READ_BUF_SIZE];
int read_val[5];
int i=0,j=0;
unsigned long reg_addr=0;
int version=200;    //Initialized with invalid version
int v16_thresh=790;
int LED_L=1,LED_R=0;

//Initialize
int init(void)
{
    int i,raw;
    if ((fd = open(fileName, O_RDWR)) < 0)
    {
        // Open port for reading and writing
        printf("Failed to open i2c port\n");
        return -1;
    }

    if (ioctl(fd, I2C_SLAVE, address) < 0)
    {
        // Set the port options and set the address of the device
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

//Sleep in ms 
void pi_sleep(int t)
{
    usleep(t*1000);
}

//Write a register
int write_block(char cmd,char v1,char v2,char v3)
{
    w_buf[0]=1;
    w_buf[1]=cmd;
    w_buf[2]=v1;
    w_buf[3]=v2;
    w_buf[4]=v3;

    ssize_t ret = write(fd, w_buf, WRITE_BUF_SIZE);
    // sleep for 1 ms to prevent too fast writing
    pi_sleep(1);

    if (ret != WRITE_BUF_SIZE) {
        if (ret == -1) {
            printf("Error writing to GoPiGo (errno %i): %s\n", errno, strerror(errno));
        }
        else {
            printf("Error writing to GoPiGo\n");
        }
        return ret;
    }
    return 1;
}

//Read 1 byte of data
char read_byte(void)
{
    int reg_size=1;
    ssize_t ret = read(fd, r_buf, reg_size);

    if (ret != reg_size) {
        if (ret == -1) {
            printf("Unable to read from GoPiGo (errno %i): %s\n", errno, strerror(errno));
        }
        else {
            printf("Unable to read from GoPiGo\n");
        }
        return -1;
    }

    return r_buf[0];
}

// Read Line Sensor Values(each 10 Bit) to the buffer
int read_sensor(void)
{      
	write_block(aRead_cmd,0,0,0);
	pi_sleep(50);
	int reg_size=10;
	ssize_t ret = read(fd, r_buf, reg_size);
	if (ret != reg_size) {
        if (ret == -1) {
            printf("Unable to read from Line Sensor (errno %i): %s\n", errno, strerror(errno));
        }
        else {
            printf("Unable to read from Line_Sensor\n");
        }
        return -1;
    }
	for(i=0;i<10;i=i+2){                    // To convert the 10 bit analog reading of each sensor to decimal and store it in read_val[]
		read_val[j]=r_buf[i]*256+r_buf[i+1];
		j++;	
	}
	j=0;
	return 0;
}

// To get Line Sensor Values(0-1024) from the read buffer
void get_sensorval(void)
{
	while(1){
		read_sensor();
		if (read_val[0]!=-1){
			for(i=0;i<5;i++){                   // To print the five IR sensor readings
				printf("%d  ",read_val[i]);
			}
                    return;
		}
			
	}
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


