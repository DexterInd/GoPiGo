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


#include "line_sensor.h"
 
int fd;
char *fileName = "/dev/i2c-1";
unsigned char w_buf[WRITE_BUF_SIZE],r_buf[READ_BUF_SIZE];
int read_val[5];
int i=0;
unsigned long reg_addr=0;

//Initialize
int init(void)
{
   
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
	
    return 1;
}

//Sleep in ms 
void sleep_ms(int t)
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
    sleep_ms(1);

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
{       int flag = 0;
	write_block(line_read_cmd,0,0,0); // This Write statement takes 0.895ms
	int reg_size=10;
	//Used to read the data from line sensor using i2c - read(int fildes, void *buf, size_t nbyte);
	ssize_t ret = read(fd, r_buf, reg_size);//This read statement takes 1.635ms to read from 5 IR sensors   
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
		read_val[i/2]=r_buf[i]*256+r_buf[i+1]; // Values less than 100 - White, Values greater than 800- Black
                if (read_val[i/2]> 65000)              // Checking for junk values in the input
			flag=1;
	}
        if (flag==1){
		for(i=0;i<5;i++)
			read_val[i]=-1;                    // Making junk input values to -1
        }        
	return 0;
}



