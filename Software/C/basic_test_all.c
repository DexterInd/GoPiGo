#include "gopigo.h"

int main(void)
{									// Buffer for data being read/ written on the i2c bus

	if ((fd = open(fileName, O_RDWR)) < 0) {					// Open port for reading and writing
		printf("Failed to open i2c port\n");
		exit(1);
	}
	
	if (ioctl(fd, I2C_SLAVE, address) < 0) {					// Set the port options and set the address of the device 
		printf("Unable to get bus access to talk to slave\n");
		exit(1);
	}

    printf("%f\n",volt());

    fwd();
    usleep(1000*1000);
    stop();
    return 0;
}