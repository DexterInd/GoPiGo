int m1a=7;
int m1b=8;
int m2a=4;
int m2b=13;
int c1=9;
int c2=12;
void setup()
{
    pinMode(m1a, OUTPUT);
    pinMode(m1b, OUTPUT);     
    pinMode(m2a, OUTPUT);  
    pinMode(m2b, OUTPUT);      
}
void loop()
{
    analogWrite(c1,100);
    analogWrite(c2,255);
    digitalWrite(m1a, LOW);                
    digitalWrite(m1b, HIGH);   
    digitalWrite(m2a, LOW);                
    digitalWrite(m2b, HIGH);
}

