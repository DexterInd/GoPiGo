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

extern int fd;
extern char *fileName;
extern int  address;
extern unsigned char w_buf[5],r_buf[32];
extern unsigned long reg_addr;

#define fw_ver_cmd 20
#define volt_cmd 118
#define fwd_cmd 119
#define stop_cmd 120

//Write a register
long write_block(char cmd,char v1,char v2,char v3);
//Read 1 byte of data
char read_byte(void);
//Get voltage
float volt(void);
//Move forward
int fwd();
//Stop
int stop();

#endif /*GOPIGO_H */
