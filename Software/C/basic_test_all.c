// ####################################################################################                                                                  
// This is the basic example to use the GoPiGo.                                
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