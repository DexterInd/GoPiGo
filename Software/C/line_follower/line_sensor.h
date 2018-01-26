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

#ifndef LINE_SENSOR_H
#define LINE_SENSOR_H

extern int fd;
extern char *fileName;
extern unsigned char w_buf[5],r_buf[32];
extern unsigned long reg_addr;
extern int read_val[5];

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
#define WRITE_BUF_SIZE       5
#define READ_BUF_SIZE        32
#define line_read_cmd        3    //analogRead() command format header
#define address              0x06 //I2C Address of Arduino

//Initialize
int init(void);

//Write a register
int write_block(char cmd,char v1,char v2,char v3);

//Read 1 byte of data
char read_byte(void);

// Read Line Sensor Values(each 10 Bit) to the buffer
int read_sensor(void);

//Sleep in ms 
void sleep_ms(int t);

#endif

