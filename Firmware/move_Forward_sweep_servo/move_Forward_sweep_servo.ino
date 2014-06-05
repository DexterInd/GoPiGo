//Make the robot move via the terminal
#include <Wire.h>
#include <Servo.h> 

 
#define SLAVE_ADDRESS 0x04
int number = 5;
int state = 0;

//Motor inputs on arduino
int i11=7;  // Control pin, motor 1
int i12=8;  // Control pin, motor 1
int i21=4;  // Control pin, motor 2
int i22=13; // Control pin, motor 2
int s_1=9;  // Pwm motor 1
int s_2=6;  // PWM motor 2
int sp=200;  // Speed of motors.

int left_led = 5;
int rite_led = 10;
 
Servo myservo;  // create servo object to control a servo 
                // a maximum of eight servo objects can be created 
 
int pos = 0;    // variable to store the servo position 

void forward()
{
  pinMode(i11, OUTPUT);     
  pinMode(i12, OUTPUT);  
  pinMode(i21, OUTPUT);     
  pinMode(i22, OUTPUT); 
  
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
  digitalWrite(i21, LOW);                
  digitalWrite(i22, LOW);
}
void right()
{
  digitalWrite(i11, LOW);                
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
    //myservo.attach(left_led);  // attaches the servo on pin 9 to the servo object 
  
    pinMode(i11, OUTPUT);     
    pinMode(i12, OUTPUT);  
    pinMode(i21, OUTPUT);     
    pinMode(i22, OUTPUT); 
    //pinMode(s_1, OUTPUT); 
    //pinMode(s_2, OUTPUT);          
     //pinMode(left_led, OUTPUT);
    pinMode(rite_led, OUTPUT);     
    Wire.begin(SLAVE_ADDRESS);

    //myservo.attach(left_led);  // attaches the servo on pin 9 to the servo object 

    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);   
}

void blink_cross_eyed(){
    //digitalWrite(left_led,HIGH);
    digitalWrite(rite_led,LOW);
    delay(500);
    //digitalWrite(left_led,LOW);
    digitalWrite(rite_led,HIGH);    
    delay(500);
  
}

void blink_both_eyes(){
    //digitalWrite(left_led,HIGH);
    digitalWrite(rite_led,HIGH);
    delay(750);
    //digitalWrite(left_led,LOW);
    digitalWrite(rite_led,LOW);    
    delay(750);
  
}

void swing_servo(){
  for(pos = 0; pos < 180; pos += 1)  // goes from 0 degrees to 180 degrees 
  {                                  // in steps of 1 degree 
    myservo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(15);                       // waits 15ms for the servo to reach the position 
  } 
  for(pos = 180; pos>=1; pos-=1)     // goes from 180 degrees to 0 degrees 
  {                                
    myservo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(15);                       // waits 15ms for the servo to reach the position 
  }   
}

void loop() {
    sp = 70;
     myservo.detach();
    analogWrite(s_1,sp);
    analogWrite(s_2,sp);

    blink_cross_eyed();
    blink_cross_eyed(); 

    forward();
    blink_cross_eyed();
    blink_cross_eyed();
    blink_cross_eyed();
    blink_cross_eyed();
    blink_cross_eyed();
    blink_cross_eyed();
    blink_cross_eyed();
    blink_cross_eyed();     
    stop();
    myservo.attach(left_led);
    swing_servo();
    myservo.detach();
    blink_cross_eyed();
    blink_cross_eyed();      
    blink_cross_eyed();
    blink_cross_eyed();     
 
 


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

