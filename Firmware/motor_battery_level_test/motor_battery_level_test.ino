#include <Wire.h>

#define SLAVE_ADDRESS 0x04
int number = 5;
int state = 0;

void setup() 
{
    analogReference(EXTERNAL);
    pinMode(13, OUTPUT);
    pinMode(2, OUTPUT);     
    pinMode(3, OUTPUT);  
    pinMode(4, OUTPUT);     
    pinMode(5, OUTPUT); 
   // Serial.begin(9600);         

    Wire.begin(SLAVE_ADDRESS);

    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);

    //Serial.println("Ready!");
}
int st=0;
void loop() 
{
  if(st==1)
  {
  analogWrite(6,255);
  analogWrite(7,255);
   digitalWrite(2, LOW);                
  digitalWrite(3, HIGH);   
  digitalWrite(4, LOW);                
  digitalWrite(5, HIGH); 
  } 
}

void receiveData(int byteCount){
    while(Wire.available()) 
    {
        number = Wire.read();
        Serial.print("data received: ");
        Serial.println(number);
     }
}

// callback for sending data
byte b[3];
int d;
void sendData(){
  st=1;
  d=analogRead(0);
  //Serial.println(d);
  b[1]=d/256;
  b[2]=d%256;
  Wire.write(b, 3);
}

