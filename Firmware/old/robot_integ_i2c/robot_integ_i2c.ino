//Firmware for all the GoPiGo Functionalities via I2C
#include <Wire.h>
#include <SoftwareServo.h>	//Not using Servo.h because it disables timers
SoftwareServo servo1;

#define SLAVE_ADDRESS 0x08	//GoPiGo Address 0x08
#define debug 0

//Pin Definitions
int i11=7;	//Motor 1 direction control pins
int i12=8;
int i21=4;	//Motor 2 direction control pins
int i22=13;
int s_1=9;	//Speed control pins
int s_2=6;
int sp=200,sp1,sp2;	//Speed control variables
int volt,pin,value;	//Voltage variables
int right_led_pin=5,left_led_pin=10;	//LED pins

int sf1=0,sf2=0,mf[2]= {0,0},td,cng_s;	//PID variables
float alpha,kp=1;
unsigned long ti1,tf1,ti2,tf2,td1,td2;

volatile int state = LOW;	//Encoder targetting variables
volatile int s=0;
volatile int f1=0,f2=0,e1=0,e2=0;
int tgt_flag=0,m1_en=0,m2_en=0,tgt=0;

volatile int cmd[5],index=0,flag=0,bytes_to_send=0;	//I2C Message variables
byte payload[3],st_flag=0;

int servo_flag=0;

//Move the GoPiGo forward
void forward()
{
	digitalWrite(i11, LOW);
	digitalWrite(i12, HIGH);
	digitalWrite(i21, LOW);
	digitalWrite(i22, HIGH);
}
//Move GoPiGo backward
void backward()
{
	digitalWrite(i11, HIGH);
	digitalWrite(i12, LOW);
	digitalWrite(i21, HIGH);
	digitalWrite(i22, LOW);
}
//Turn GoPiGo Left slow (one motor off, better control)
void left()
{
	digitalWrite(i11, LOW);
	digitalWrite(i12, HIGH);
	digitalWrite(i21, HIGH);
	digitalWrite(i22, HIGH);
}
//Rotate GoPiGo left in same position
void left_rot()
{
	digitalWrite(i11, LOW);
	digitalWrite(i12, HIGH);
	digitalWrite(i21, HIGH);
	digitalWrite(i22, LOW);
}
//Turn GoPiGo right slow (one motor off, better control)
void right()
{
	digitalWrite(i11, HIGH);
	digitalWrite(i12, HIGH);
	digitalWrite(i21, LOW);
	digitalWrite(i22, HIGH);
}
//Rotate GoPiGo right in same position
void right_rot()
{
	digitalWrite(i11, HIGH);
	digitalWrite(i12, LOW);
	digitalWrite(i21, LOW);
	digitalWrite(i22, HIGH);
}
//Stop the GoPiGo
void stp()
{
	digitalWrite(i11, HIGH);
	digitalWrite(i12, HIGH);
	digitalWrite(i21, HIGH);
	digitalWrite(i22, HIGH);
}
//Set the LED status and power
//	pin:	0-right led
//			1-left led
//	pow:	PWM power
void led_light(int pin,int pow)
{
	if(pin==0)//right
	{
		analogWrite(right_led_pin,pow);
	}
	else//left
	{
		analogWrite(left_led_pin,pow);
	}
}
//Setting up the GoPiGo
void setup()
{
	if (debug)
	{
		Serial.begin(9600);
		Serial.print("Ready");
	}
	attachInterrupt(1, step1, RISING);	//For encoders
	attachInterrupt(0, step2, RISING);
	
	pinMode(i11, OUTPUT);	//Attach motoe direction control pins
	pinMode(i12, OUTPUT);
	pinMode(i21, OUTPUT);
	pinMode(i22, OUTPUT);
	
	servo1.attach(5);	//Set up the Servo
	servo1.setMaximumPulse(2200);
	
	Wire.begin(SLAVE_ADDRESS);	//Set up I2C
	Wire.onReceive(receiveData);
	Wire.onRequest(sendData);
	
	sp1=sp2=sp;
}
void loop()
{
	analogWrite(s_1,sp1);	//Write the speed to the motors
	analogWrite(s_2,sp2);
	
	if(cmd[0]==119 || cmd[0]==115)	//If movin with PID is being used
	{
		if(f1==1)
		{
			if(sf1==0)
			{
				sf1=1;
				ti1=micros();
			}
			else
			{
				sf1=0;
				tf1=micros();
				td1=tf1-ti1;
				mf[0]=1;
			}
			f1=0;
		}
		if(f2==1)//for enc 2
		{
			if(sf2==0)//if second value
			{
				sf2=1;
				ti2=micros();
			}
			else
			{
				sf2=0;
				tf2=micros();
				td2=tf2-ti2;
				mf[1]=1;
			}
			f2=0;
		}
		if(mf[0]==1)// && mf[1]==1)
			if(td1>10000)// &&td2>10000)
			{
				td=td2-td1;
				alpha=(float)kp*td/td1;
				cng_s=-alpha*sp1;
				sp2=sp1+cng_s;
				sp2=sp2>255?255:sp2;
				sp2=sp2<0?0:sp2;
				mf[0]=mf[1]=0;
			}
	}
	if(cmd[0]==116) //'t': Increase hte speed
	{
		if(sp1>244)
			sp1=255;
		else
			sp1=sp1+10;
		cmd[0]=0;
	}
	if(cmd[0]==103) //'g': Decrease the speed
	{
		if(sp1<11)
			sp1=0;
		else
			sp1=sp1-10;
		cmd[0] =0;
	}
	sp2=sp1;
	if(cmd[0]==119 || cmd[0]==105)  //Enable the motors t move forward 'w'-pid, 'i'-nopid
		forward();
	else if(cmd[0]==97) //'a': Turn left	
		left();
	else if(cmd[0]==98) //'b': Rotate left
		left_rot();
	else if(cmd[0]==115 || cmd[0]==107) //Enable the motors t move backward 's'-pid 'k'-nopid
		backward();
	else if(cmd[0]==100)  //'d': Trun right
		right();
	else if(cmd[0]==110)  //'n': Turn left
		right_rot();
	else if(cmd[0]==120)  //'x': Stop
		stp();
	else if(cmd[0]==118) //'v': Read voltage
	{
		volt=analogRead(0);
		payload[0]=volt/256;
		payload[1]=volt%256;
		bytes_to_send=2;
		cmd[0]=0;
	}
	else if(cmd[0]==117) //Read ultrasonic sensor
	{
		int _pin=cmd[1];
		if(debug)
		{
			Serial.print("US ");
			Serial.print(_pin);
		}
		pinMode(_pin, OUTPUT);
		digitalWrite(_pin, LOW);
		delayMicroseconds(2);
		digitalWrite(_pin, HIGH);
		delayMicroseconds(5);
		digitalWrite(_pin,LOW);
		pinMode(_pin,INPUT);
		long dur = pulseIn(_pin,HIGH);
		int RangeCm = dur/29/2;

		payload[0]=RangeCm/256;
		payload[1]=RangeCm%256;
		bytes_to_send=2;
		if(debug)
		{
			Serial.print(RangeCm);
			Serial.print(" ");
			Serial.print(payload[0]);
			Serial.print(" ");
			Serial.println(payload[1]);
		}
		cmd[0]=0;
	}
	else if(cmd[0]==108)//LED light 'l'
	{
		//cmd[1]: 	pin(0-right,1-left LED)
		//cmd[2]:	PWM power (0-255)
		led_light(cmd[1],cmd[2]);
		cmd[0]=0;
	}
	else if(cmd[0]==101) //Servo
	{
		value=cmd[1];
		if(debug)
		{
			Serial.println(value);
		}
		servo1.write(value);
		servo_flag=1;

		cmd[0]=0;
	}
	if(cmd[0]==50 || tgt_flag==1)//Encoder targetting
	{
		if(cmd[0]==50)
		{
			cmd[0]=0;
			tgt_flag=1;
			m1_en=cmd[1]/2;
			m2_en=cmd[1]%2;
			tgt=cmd[2]*256+cmd[3];
			e1=e2=0;
		}
		if(m1_en && !m2_en)
		{
			if(e1>=tgt)
			{
				cmd[0]=0;
				stp();
				tgt_flag=0;
			}
		}
		else if(!m1_en && m2_en)
		{
			if(e2>=tgt)
			{
				cmd[0]=0;
				stp();
				tgt_flag=0;
			}
		}
		else if(m1_en && m2_en)
		{
			if(e1>=tgt && e2>=tgt)
			{
				cmd[0]=0;
				stp();
				tgt_flag=0;
			}
		}
		if(debug)
		{
			Serial.print(cmd[1]);
			Serial.print(" ");
			Serial.print(cmd[2]);
			Serial.print(" ");
			Serial.print(cmd[3]);
			Serial.print(" ");
			Serial.print(e1);
			Serial.print(" ");
			Serial.print(e2);
			Serial.print(" ");
			Serial.print(bytes_to_send);
			Serial.print(" ");
			Serial.print(tgt_flag);
			Serial.print(" ");
			Serial.println(tgt);
		}
	}
	if(servo_flag)	//Keep refreshing for software servo
		SoftwareServo::refresh();
}
//Recieve commands via I2C
void receiveData(int byteCount)
{
	while(Wire.available())
	{
		if(Wire.available()==4)
		{
			flag=0;
			index=0;
		}
		cmd[index++] = Wire.read();
	}
}
// callback for sending data
volatile int ind=0;
void sendData()
{
	if(bytes_to_send==2)
	{
		Wire.write(payload[ind++]);
		if(ind==2)
		{
			ind=0;
			bytes_to_send=0;
		}
	}
	else if(tgt_flag)
	{
		Wire.write(tgt_flag);
	}
}
//Encoder ISR's
void step1()
{
	e1++;
	f1=1;
}
void step2()
{
	e2++;
	f2=1;
}
