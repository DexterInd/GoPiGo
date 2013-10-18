//Make the robot move via the terminal
#include <Wire.h>

#define SLAVE_ADDRESS 0x04
int number = 5;
int state = 0;

//Motor inputs on arduino
int i11=2;
int i12=3;
int i21=4;
int i22=5;
int s_1=6;
int s_2=9;

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
    pinMode(13, OUTPUT);
    pinMode(i11, OUTPUT);     
    pinMode(i12, OUTPUT);  
    pinMode(i21, OUTPUT);     
    pinMode(i22, OUTPUT); 
   // pinMode(s_1, OUTPUT); 
    //pinMode(s_2, OUTPUT); 
    Serial.begin(9600);         

    Wire.begin(SLAVE_ADDRESS);

    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);

    Serial.println("Ready!");
     
}

void loop() {
    analogWrite(6,255);
    analogWrite(7,255);
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
    //delay(100);
}

void receiveData(int byteCount){

    while(Wire.available()) 
    {
        number = Wire.read();
        digitalWrite(13,HIGH);
        delay(50);
        digitalWrite(13,LOW);
        Serial.print("data received: ");
        Serial.println(number);
     }
}

// callback for sending data
void sendData(){
    Wire.write(number);
}

