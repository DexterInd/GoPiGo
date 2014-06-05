//Make the robot move via the terminal
#include <Wire.h>

#define SLAVE_ADDRESS 0x04
int number = 5;
int state = 0;

//Motor inputs on arduino
int i11=7;
int i12=8;
int i21=4;
int i22=13;
int s_1=9;
int s_2=6;
int sp=200;
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
  digitalWrite(i22, LOW);
}
void right()
{
  digitalWrite(i11, HIGH);                
  digitalWrite(i12, LOW);
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

void setup() {
    pinMode(i11, OUTPUT);     
    pinMode(i12, OUTPUT);  
    pinMode(i21, OUTPUT);     
    pinMode(i22, OUTPUT); 
    //pinMode(s_1, OUTPUT); 
    //pinMode(s_2, OUTPUT);          
     pinMode(5, OUTPUT);
    Wire.begin(SLAVE_ADDRESS);

    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);   
}

void loop() {
    analogWrite(s_1,sp);
    analogWrite(s_2,sp);
    if(number==116) //t
    {
      if(sp>244)
        sp=255;
      else
        sp=sp+10;
      number=0;
    }
    if(number==103) //g
    {
      if(sp<11)
        sp=0;
      else
        sp=sp-10;
      number =0;
    }
    if(sp>255)
      sp=255;
    if(sp<0)
      sp=0;
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
    digitalWrite(5,HIGH);
    delay(100);
    digitalWrite(5,LOW);
     delay(100);
}

void receiveData(int byteCount){

    while(Wire.available()) 
    {
        number = Wire.read();    
        
     }
}

// callback for sending data
void sendData(){
    Wire.write(number);
}

