//Code for testing interrupts for the encoder signal
volatile int state = LOW;
volatile int s1=0,s2=0;
int i11=7;
int i12=8;
int i21=4;
int i22=13;
int s_1=9;
int s_2=6;
int sp1=200;
void f(int m)
{
    if(m==1)
    {
	digitalWrite(i11, LOW);                
	digitalWrite(i12, HIGH);   
    }
    if(m==2)
    {
        digitalWrite(i21, LOW);                
	digitalWrite(i22, HIGH); 
    }
}
void b(int m)
{
    if(m==1)
    {
	digitalWrite(i11, HIGH);                
	digitalWrite(i12, LOW);   
    }
    if(m==2)
    {
        digitalWrite(i21, HIGH);                
	digitalWrite(i22, LOW); 
    }
}
void s(int m)
{
     if(m==1)
     {
	digitalWrite(i11, HIGH);                
	digitalWrite(i12, HIGH);
      }
      if(m==2)
      {
        digitalWrite(i21, HIGH);                
	digitalWrite(i22, HIGH);
      }
}
void motor_speed(int motor, int spd)
{
  if(motor==1)
    analogWrite(s_1,spd);
  if(motor==2)
    analogWrite(s_2,spd);
}
int mot=1;
void setup()
{
  delay(5000);
  Serial.begin(115200);
  pinMode(i11, OUTPUT);     
  pinMode(i12, OUTPUT);  
  pinMode(i21, OUTPUT);     
  pinMode(i22, OUTPUT);
  attachInterrupt(1, step1, RISING);
  attachInterrupt(0, step2, RISING);
}
int flag=1;
void loop()
{
  if(flag)
  {
    b(mot);
    flag=0;
  }
  motor_speed(mot,sp1);
  if(s2==72)
  {
    f(mot);
    delay(20);
    s(mot);
  }
  Serial.print(s1);
  Serial.print(" ");
  Serial.println(s2);
  delay(10);
}
void step1()
{
  s1++;
}
void step2()
{
  s2++;
}
