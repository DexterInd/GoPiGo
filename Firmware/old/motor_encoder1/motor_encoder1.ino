//Code for testing interrupts for the encoder signal
volatile int state = LOW;
volatile int s=0;
volatile int f=0,f1=0;
int i11=7;
int i12=8;
int i21=4;
int i22=13;
int s_1=9;
int s_2=6;
int sp=140;
void forward()
{
  digitalWrite(i11, LOW);                
  digitalWrite(i12, HIGH);   
  digitalWrite(i21, LOW);                
  digitalWrite(i22, HIGH); 
}
void setup()
{
  attachInterrupt(0, step1, RISING);
  attachInterrupt(1, step2, RISING);
  pinMode(i11, OUTPUT);     
  pinMode(i12, OUTPUT);  
  pinMode(i21, OUTPUT);     
  pinMode(i22, OUTPUT); 
  pinMode(10,OUTPUT);
  pinMode(11,OUTPUT);
  forward();
  analogWrite(s_1,sp);
  analogWrite(s_2,sp);
}
void loop()
{
  
  
  if(f%18==0)
    digitalWrite(10,HIGH);
  if(f1%18==0)
    digitalWrite(11,HIGH);
  //f1=f=0;
  delay(10);
  digitalWrite(10,LOW);
  digitalWrite(11,LOW);
  
}
void step1()
{
  f++;
}
void step2()
{
  f1++;
}

