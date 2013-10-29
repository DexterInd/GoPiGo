void setup() 
{              
  pinMode(0, OUTPUT);
  pinMode(1, OUTPUT);
  pinMode(5, OUTPUT);  
  pinMode(11, OUTPUT);
   pinMode(12, OUTPUT);
   pinMode(13, OUTPUT);
   pinMode(A3, OUTPUT);
   pinMode(A1, OUTPUT);
   pinMode(A2, OUTPUT);
}
int a0,a1,a2,a3;
void loop() 
{
digitalWrite(A3, HIGH); 
digitalWrite(A1, HIGH); 
digitalWrite(A2, HIGH); 
digitalWrite(0, HIGH); 
digitalWrite(1, HIGH);          
digitalWrite(5, HIGH); 
digitalWrite(11, HIGH); 
digitalWrite(12, HIGH);
digitalWrite(13, HIGH);

delay(100);
digitalWrite(A3, LOW); 
digitalWrite(A1, LOW);
digitalWrite(A2, LOW);
digitalWrite(0, LOW); 
digitalWrite(1, LOW);          
digitalWrite(5, LOW); 
digitalWrite(11, LOW); 
digitalWrite(12, LOW); 
digitalWrite(13, LOW);
delay(100);
}
