//Proportional working
volatile int state = LOW;
volatile int s=0;
volatile int f1=0,f2=0;
int i11=7;
int i12=8;
int i21=4;
int i22=13;
int s_1=9;
int s_2=6;
int sp1=170;
int sp2=170;

void forward()
{
  digitalWrite(i11, LOW);                
  digitalWrite(i12, HIGH);   
  digitalWrite(i21, LOW);                
  digitalWrite(i22, HIGH); 
}

void setup()
{
  Serial.begin(115200);
  attachInterrupt(0, step1, RISING);
  attachInterrupt(1, step2, RISING);
  pinMode(i11, OUTPUT);     
  pinMode(i12, OUTPUT);  
  pinMode(i21, OUTPUT);     
  pinMode(i22, OUTPUT); 
  forward();
  analogWrite(s_1,sp1);
  analogWrite(s_2,sp2);
  delay(300);
}
int sf1=0,sf2=0,mf[2]={0,0},td,cng_s;
float alpha,kp=1;
unsigned long ti1,tf1,ti2,tf2,td1,td2;
void loop()
{
  kp=analogRead(A1);
  kp/=500;
  //Serial.println(kp);
  analogWrite(s_1,sp1);
  analogWrite(s_2,sp2);
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
      //Serial.print("tdiff1: ");
      //Serial.println(td1);
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
      //Serial.print("tdiff2: ");
      //Serial.println(td2);
      mf[1]=1;
    }
    f2=0;
  }
  if(mf[0]==1 && mf[1]==1)
    if(td1>10000 &&td2>10000)
    {
      td=td2-td1;
      alpha=(float)kp*td/td1;
      cng_s=-alpha*sp1;
      sp2+=cng_s;
      sp2=sp2>255?255:sp2;
      sp2=sp2<0?0:sp2;
      Serial.print("tdiff1: ");
      Serial.println(td1);
      Serial.print("tdiff2: ");
      Serial.println(td2);
      Serial.print("s1 ");
      Serial.print(sp1);
      Serial.print(" s2 ");
      Serial.print(sp2);
      Serial.print(" cng_s ");
      Serial.println(cng_s);
       Serial.println("");
      mf[0]=mf[1]=0;
    }
}
void step1()
{
  f1=1;
}
void step2()
{
  f2=1;
}

