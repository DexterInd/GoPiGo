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

int main(void){
    int i;                                 //Program to read IR sensor values
    printf("IR Sensor Values \n");
    printf("IR1  IR2  IR3  IR4  IR5\n");	
    if(init()==-1)
        exit(1);
    while(1){
	read_sensor();
        printf("\n");
	for(i=0;i<5;i++){                    // To convert the 10 bit analog reading of each sensor to decimal and store it in read_val[]
                printf("%d ",read_val[i]);  // Values less than 100 - White, Values greater than 800- Black, Value -1 -Error

        }
	//sleep_ms(500); // Uncomment the sleep_ms() if the values run fast on the screen 
    }
    return 0;
}

