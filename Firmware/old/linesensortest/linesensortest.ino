#include <Wire.h>

#define SLAVE_ADDRESS 0x04
int number = 0;
int state = 0;

byte b[7];
int aRead1=0, aRead2=0,aRead3=0;

void setup() {
    Wire.begin(SLAVE_ADDRESS);
    Wire.onRequest(sendData);
}

void loop()
{
  aRead1=analogRead(1);
  aRead2=analogRead(2);
  aRead3=analogRead(3);
  
  b[1]=aRead1/256;
  b[2]=aRead1%256;
  b[3]=aRead2/256;
  b[4]=aRead2%256;
  b[5]=aRead3/256;
  b[6]=aRead3%256;
}


void sendData()
{
    Wire.write(b, 7);
}

