//Code for encoder testing- Rotate the wheels with hand to make the LED's blink
volatile int state = LOW;
volatile int s=0;
volatile int f=0,f1=0;
int i11=7;
int i12=8;
int i21=4;
int i22=13;
void setup()
{
  pinMode(i11, OUTPUT);     
  pinMode(i12, OUTPUT);  
  pinMode(i21, OUTPUT);     
  pinMode(i22, OUTPUT); 
  attachInterrupt(0, step1, CHANGE);
  attachInterrupt(1, step2, CHANGE);
  pinMode(10,OUTPUT);
  pinMode(5,OUTPUT);
}
void loop()
{
  if(f==1)
    digitalWrite(10,HIGH);
  if(f1==1)
    digitalWrite(5,HIGH);
  f1=f=0;
  delay(50);
  digitalWrite(10,LOW);
  digitalWrite(5,LOW);
}
void step1()
{
  f=1;
}
void step2()
{
  f1=1;
}

