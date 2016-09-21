// ####################################################################################                                                             
// This is the basic example to use the Line Sensor.
//http://www.dexterindustries.com/GoPiGo/gopigo-line-follower-getting-started/
//
// History
// ------------------------------------------------
// Date                 Comments
// 21 Sep 16            Initial Authoring

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

int main(void){                                 //Program to read IR sensor values
    printf("IR Sensor Values \n");
	printf("IR1  IR2  IR3  IR4  IR5\n");	
	if(init()==-1)
        exit(1);
	while(1){
		get_sensorval();
		printf("\n");
		pi_sleep(500);
	}
	return 0;
}

