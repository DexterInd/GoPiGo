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
    usleep(100000);
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
