//Make the robot move via the terminal
#include <Wire.h>
#include <SoftwareServo.h>
SoftwareServo servo1;

#define SLAVE_ADDRESS 0x04
int number = 5;

//Motor inputs on arduino
int i11=7;
int i12=8;
int i21=4;
int i22=13;
int s_1=9;
int s_2=6;
int sp=200,sp1,sp2;
int volt,pin,value;

int sf1=0,sf2=0,mf[2]={0,0},td,cng_s;
float alpha,kp=1;
unsigned long ti1,tf1,ti2,tf2,td1,td2;

volatile int state = LOW;
volatile int s=0;
volatile int f1=0,f2=0;
void forward()
{
	digitalWrite(i11, LOW);                
	digitalWrite(i12, HIGH);   
	digitalWrite(i21, LOW);                
	digitalWrite(i22, HIGH); 
}
void backward()
{
	digitalWrite(i11, HIGH);                
	digitalWrite(i12, LOW);   
	digitalWrite(i21, HIGH);                
	digitalWrite(i22, LOW); 
}
void left()
{
	digitalWrite(i11, LOW);                
	digitalWrite(i12, HIGH); 
	digitalWrite(i21, HIGH);                
	digitalWrite(i22, HIGH);
}
void right()
{
	digitalWrite(i11, HIGH);                
	digitalWrite(i12, HIGH);
	digitalWrite(i21, LOW);                
	digitalWrite(i22, HIGH); 
}
void stop()
{
	digitalWrite(i11, HIGH);                
	digitalWrite(i12, HIGH);
	digitalWrite(i21, HIGH);                
 	digitalWrite(i22, HIGH); 
}

void setup() 
{
  Serial.begin(9600);
  attachInterrupt(0, step1, RISING);
  attachInterrupt(1, step2, RISING);
    pinMode(i11, OUTPUT);     
    pinMode(i12, OUTPUT);  
    pinMode(i21, OUTPUT);     
    pinMode(i22, OUTPUT);           
    pinMode(5, OUTPUT);
    servo1.attach(10);
    servo1.setMaximumPulse(2200);
   // Wire.begin(SLAVE_ADDRESS);

  //  Wire.onReceive(receiveData);
  //  Wire.onRequest(sendData);   
	sp1=sp2=sp;
}
int prev_number=0;
void loop() 
{
  prev_number=number;
  if(Serial.available()>0)
    number=Serial.read();	
  analogWrite(s_1,sp1);
  analogWrite(s_2,sp2);
  if(number==119 || number==115)
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
      /*Serial.print("tdiff1: ");
      Serial.println(td1);
      Serial.print("tdiff2: ");
      Serial.println(td2);
      Serial.print("s1 ");
      Serial.print(sp1);
      Serial.print(" s2 ");
      Serial.print(sp2);
      Serial.print(" cng_s ");
      Serial.println(cng_s);
       Serial.println("");*/
      mf[0]=mf[1]=0;
    }
  }
  if(number==116) //t
    {
      if(sp1>244)
        sp1=255;
      else
        sp1=sp1+10;
      number=0;
    }
  if(number==103) //g
    {
      if(sp1<11)
        sp1=0;
      else
        sp1=sp1-10;
      number =0;
    }
    sp2=sp1;
    if(number==119)  //w
      forward();
    else if(number==97) //a
      left();
    else if(number==115) //s
      backward();
    else if(number==100)  //d
      right();
    else if(number==120)  //x
      stop();
    else if(number==118) //v
    {
      volt=analogRead(0);
      Serial.print(volt);
      number=0;
    }
    if(number==117) //ultrasonic
  {
    while(1)
      if(Serial.available())
      {
        pin=Serial.read(); 
        break;
      }
    pinMode(pin, OUTPUT);
    digitalWrite(pin, LOW);
    delayMicroseconds(2);
    digitalWrite(pin, HIGH);
    delayMicroseconds(5);
    digitalWrite(pin,LOW);
    pinMode(pin,INPUT);
    int dur = pulseIn(pin,HIGH);
    int RangeCm = dur/29/2;
    Serial.print(RangeCm);
    number=0;
  }
  if(number==98)
  {
    while(1)
      if(Serial.available())
      {
        value=Serial.read(); 
        break;
      }
    servo1.write(value);
    SoftwareServo::refresh();
    number=0;
  }
  //delay(300);
}
/*void receiveData(int byteCount){
    while(Wire.available()) 
    {
        number = Wire.read();    
    }
}
// callback for sending data
void sendData(){
    Wire.write(number);
}*/
void step1()
{
  f1=1;
}
void step2()
{
  f2=1;
}
