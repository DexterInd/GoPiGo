// ####################################################################################                                                             
// This is the basic example to use the GoPiGo.
// http://www.dexterindustries.com/GoPiGo/
// History
// ------------------------------------------------
// Date                 Comments
// 30 Aug 15            Initial Authoring

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
	if(init()==-1)
		exit(1);


	while(1)
	{
	   char input[2];                    /* Store 2 input characters */

	   printf("Enter cmd: ");
	   scanf(" %c", input);

	   switch (input[0])
	   {
	    	case 'w': case 'W':
	       		fwd();
	       		break;

	    	case 'a': case 'A':
	       		left();
	       		break;

	    	case 'd': case 'D':
	       		right();
	       		break;

	       	case 's': case 'S':
	       		bwd();
	       		break;

	       	case 'e': case 'E':
	       		increase_speed();
	       		break;

	       	case 'g': case 'G':
	       		decrease_speed();
	       		break;

	       	case 'z': case 'Z':
	       		exit(0);
	       		break;

	       	case 'x': case 'X':
	       		stop();
	       		break;

	       	case 'i': case 'I':
	       		motor_fwd();
	       		break;

	       	case 'k': case 'K':
	       		motor_bwd();
	       		break;

	       	case 'n': case 'N':
	       		left_rot();
	       		break;

	       	case 'm': case 'M':
	       		right_rot();
	       		break;
			
			case 'u': case 'U':
	       		printf("Ultrasonic Dist: %d\n",us_dist(15));
	       		break;
				
	       	case 't': case 'T':
	       		switch(input[1])
				{
	       			case 'r': case 'R':
	       				;
					int val = trim_read();
	       				if(val == -3){
	       					printf("-3, Trim Value Not set\n");
	       				}
	       				else{
	       					printf("%d\n", val-100);
	       				}
	       				break;
	       			case 'w': case 'W':
	       				;
					int val2;
	       				printf("Enter trim value to write to EEPROM(-100 to 100):\n");
	   					scanf(" %d", &val2);
	   					trim_write(val2);
	   					usleep(1000*100);
	   					printf("Value in EEPROM: %d\n", trim_read()-100);
	   					break;
	   				case 't': case 'T':
	       				;
					int val3;
	       				printf("Enter trim value to test(-100 to 100):\n");
	   					scanf(" %d", &val3);
	   					trim_test(val3);
	   					usleep(1000*100);
	   					printf("Value in EEPROM: %d\n", trim_read()-100);
	   					break;
	   				default:
			       		printf("invalid trim command...\n");
			       		break;
	       		}
	       		break;

	     	default:
	       		printf("invalid command...\n");
	       		break;
	   }

	}
   	return 0;
}
