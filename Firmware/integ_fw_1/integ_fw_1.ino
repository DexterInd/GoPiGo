//Firmware for all the GoPiGo Functionalities via I2C
#include <Wire.h>
#include <SoftwareServo.h>  //Not using Servo.h because it disables timers
SoftwareServo servo1;

#define GOPIGO_ADDR 0x08    //GoPiGo Address 0x08
#define debug 1

#define ver 9              //Firmware version (12 ->1.2)
//Command list
#define fwd_cmd         119
#define motor_fwd_cmd   105
#define bwd_cmd         115
#define motor_bwd_cmd   107
#define left_cmd        97
#define left_rot_cmd    98
#define right_cmd       100
#define right_rot_cmd   110
#define stop_cmd        120
#define inc_speed_cmd   116
#define dec_speed_cmd   103
#define volt_cmd        118
#define us_cmd          117
#define led_cmd         108
#define servo_cmd       101
#define enc_tgt_cmd     50
#define fw_ver_cmd      20
#define en_enc_cmd      51
#define dis_enc_cmd     52
#define en_servo_cmd    61
#define dis_servo_cmd   60
#define set_r_speed_cmd 71
#define set_l_speed_cmd 70
#define enc_test        10
#define serial_test     11
#define digial_write    12
#define en_com_timeout_cmd  80
#define dis_com_timeout_cmd 81
#define timeout_status_cmd  82
//Pin Definitions
int motor1_control_pin1=7;      //Motor 1 direction control pins
int motor1_control_pin2=8;
int motor2_control_pin1=4;      //Motor 2 direction control pins
int motor2_control_pin2=13;
int motor1_speed_pin=9;         //Speed control pins
int motor2_speed_pin=6;
int spd=200,speed1,speed2;    //Speed control variables

int right_led_pin=5,left_led_pin=10;    //LED pins

int volt,led_pin,value;         //Voltage variables

int sf1=0,sf2=0,mf[2]= {0,0},td,cng_s;  //PID variables
float alpha=1,kp=1;
unsigned long ti1,tf1,ti2,tf2,td1,td2;

volatile int state = LOW;       //Encoder targetting variables
volatile int s=0;
volatile int f1=0,f2=0,e1=0,e2=0;
int tgt_flag=0,m1_en=0,m2_en=0,tgt=0;

volatile unsigned long last_t=0;
unsigned long timeout=0;
int timeout_f=0;

volatile int cmd[5],index=0,flag=0,bytes_to_send=0; //I2C Message variables
byte payload[3];

int servo_flag=0;

int status_r=0;
//Move the GoPiGo forward
void forward()
{
    digitalWrite(motor1_control_pin1, LOW);
    digitalWrite(motor1_control_pin2, HIGH);
    digitalWrite(motor2_control_pin1, LOW);
    digitalWrite(motor2_control_pin2, HIGH);
}
//Move GoPiGo backward
void backward()
{
    digitalWrite(motor1_control_pin1, HIGH);
    digitalWrite(motor1_control_pin2, LOW);
    digitalWrite(motor2_control_pin1, HIGH);
    digitalWrite(motor2_control_pin2, LOW);
}
//Turn GoPiGo Left slow (one motor off, better control)
void left()
{
    digitalWrite(motor1_control_pin1, LOW);
    digitalWrite(motor1_control_pin2, HIGH);
    digitalWrite(motor2_control_pin1, HIGH);
    digitalWrite(motor2_control_pin2, HIGH);
}
//Rotate GoPiGo left in same position
void left_rot()
{
    digitalWrite(motor1_control_pin1, LOW);
    digitalWrite(motor1_control_pin2, HIGH);
    digitalWrite(motor2_control_pin1, HIGH);
    digitalWrite(motor2_control_pin2, LOW);
}
//Turn GoPiGo right slow (one motor off, better control)
void right()
{
    digitalWrite(motor1_control_pin1, HIGH);
    digitalWrite(motor1_control_pin2, HIGH);
    digitalWrite(motor2_control_pin1, LOW);
    digitalWrite(motor2_control_pin2, HIGH);
}
//Rotate GoPiGo right in same position
void right_rot()
{
    digitalWrite(motor1_control_pin1, HIGH);
    digitalWrite(motor1_control_pin2, LOW);
    digitalWrite(motor2_control_pin1, LOW);
    digitalWrite(motor2_control_pin2, HIGH);
}
//Stop the GoPiGo
void stp()
{
    digitalWrite(motor1_control_pin1, HIGH);
    digitalWrite(motor1_control_pin2, HIGH);
    digitalWrite(motor2_control_pin1, HIGH);
    digitalWrite(motor2_control_pin2, HIGH);
}
//Set the LED status and power
//  led_pin:0-right led
//          1-left led
//  pow:    PWM power
void led_light(int led_pin,int pow)
{
    if(led_pin==0)//right
    {
        analogWrite(right_led_pin,pow);
    }
    else//left
    {
        analogWrite(left_led_pin,pow);
    }
}
//Setting up the GoPiGo
void setup()
{
    if (debug)
    {
        Serial.begin(115200);
        Serial.print("Ready");
    }
    
    attachInterrupt(0, step1, RISING);      //For encoders
    attachInterrupt(1, step2, RISING);
    
    pinMode(motor1_control_pin1, OUTPUT);   //Attach motor direction control pins
    pinMode(motor1_control_pin2, OUTPUT);
    pinMode(motor2_control_pin1, OUTPUT);
    pinMode(motor2_control_pin2, OUTPUT);
    
    servo1.attach(5);                       //Set up the Servo
    servo1.setMaximumPulse(2200);
    
    Wire.begin(GOPIGO_ADDR);                //Set up I2C
    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);
    
    speed1=speed2=spd;
}
void loop()
{
    
    analogWrite(motor1_speed_pin,speed1);   //Write the speed to the motors
    analogWrite(motor2_speed_pin,speed2);
    
    if(cmd[0]==enc_test)                //LED encoder test
    {
            if(f1==1)
        {
                  led_light(0,255);
                  f1=0;
            }
            if(f2==1)
        {
                  led_light(1,255);
                  f2=0;
            }
            delay(200);
            led_light(0,0);
            led_light(1,0);
    }
    if(cmd[0]==serial_test)             //Serial test
    {
      Serial.begin(9600);
      while (1)
      {
        if(Serial.available())
        {
          char c=Serial.read();
          if (c=='a')
            Serial.write('k');
          break; 
        }
      }
      Serial.end();
    }
    if(cmd[0]==digial_write)            //Digital Write
    {
      pinMode(cmd[1],OUTPUT);
      digitalWrite(cmd[1],cmd[2]);
    }
    if(cmd[0]==fwd_cmd || cmd[0]==bwd_cmd)  //If moving with PID is being used
    {
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
                mf[1]=1;
            }
            f2=0;
        }
        if(mf[0]==1)// && mf[1]==1)
            if(td1>10000)// &&td2>10000)
            {
                td=td2-td1;
                alpha=(float)kp*td/td1;
                cng_s=-alpha*speed1;
                speed2=speed2+cng_s;
                speed2=speed2>255?255:speed2;
                speed2=speed2<0?0:speed2;
                mf[0]=mf[1]=0;
                /*Serial.print("tdiff1: ");
                Serial.println(td1);
                Serial.print("tdiff2: ");
                Serial.println(td2);
                Serial.print("s1 ");
                Serial.print(speed1);
                Serial.print(" s2 ");
                Serial.print(speed2);
                Serial.print(" cng_s ");
                Serial.println(cng_s);
                Serial.println("");*/
            }
    }
    if(cmd[0]==inc_speed_cmd) //'t': Increase hte speed
    {
        if(speed1>244)
            speed1=255;
        else
            speed1=speed1+10;
        speed2=speed1;
        cmd[0]=0;
    }
    else if(cmd[0]==dec_speed_cmd) //'g': Decrease the speed
    {
        if(speed1<11)
            speed1=0;
        else
            speed1=speed1-10;
        speed2=speed1;
        cmd[0] =0;
    }
    if(cmd[0]==set_r_speed_cmd)
    {
      speed1=cmd[1];
      cmd[0]=0;
    }
    else if(cmd[0]==set_l_speed_cmd)
    {
      speed2=cmd[1];
      cmd[0]=0;
    }
    if(cmd[0]==fwd_cmd || cmd[0]==motor_fwd_cmd)    //Enable the motors t move forward 'w'-pid, 'i'-nopid
        forward();
    else if(cmd[0]==left_cmd)                       //'a': Turn left  
        left();
    else if(cmd[0]==left_rot_cmd)                   //'b': Rotate left
        left_rot();
    else if(cmd[0]==bwd_cmd || cmd[0]==motor_bwd_cmd)   //Enable the motors t move backward 's'-pid 'k'-nopid
        backward();
    else if(cmd[0]==right_cmd)                      //'d': Trun right
        right();
    else if(cmd[0]==right_rot_cmd)                  //'n': Right Rotate
        right_rot();
    else if(cmd[0]==stop_cmd)                       //'x': Stop
        stp();
    else if(cmd[0]==volt_cmd)                       //'v': Read voltage
    {
        volt=analogRead(0);
        payload[0]=volt/256;
        payload[1]=volt%256;
        bytes_to_send=2;
        cmd[0]=0;
    }
    else if(cmd[0]==us_cmd) //Read ultrasonic sensor
    {
        int _pin=cmd[1];
        if(debug)
        {
            Serial.print("US ");
            Serial.print(_pin);
        }
        pinMode(_pin, OUTPUT);
        digitalWrite(_pin, LOW);
        delayMicroseconds(2);
        digitalWrite(_pin, HIGH);
        delayMicroseconds(5);
        digitalWrite(_pin,LOW);
        pinMode(_pin,INPUT);
        long dur = pulseIn(_pin,HIGH);
        int RangeCm = dur/29/2;

        payload[0]=RangeCm/256;
        payload[1]=RangeCm%256;
        bytes_to_send=2;
        if(debug)
        {
            Serial.print(RangeCm);
            Serial.print(" ");
            Serial.print(payload[0]);
            Serial.print(" ");
            Serial.println(payload[1]);
        }
        cmd[0]=0;
    }
    else if(cmd[0]==led_cmd)//LED light 'l'
    {
        //cmd[1]:   led_pin(0-right,1-left LED)
        //cmd[2]:   PWM power (0-255)
        led_light(cmd[1],cmd[2]);
        cmd[0]=0;
    }
    else if(cmd[0]==servo_cmd) //Servo
    {
        value=cmd[1];
        if(debug)
        {
            Serial.println(value);
        }
        servo1.write(value);
        servo_flag=1;
        cmd[0]=0;
    }
    else if(cmd[0]==fw_ver_cmd)
    {
        payload[0]=ver;
        bytes_to_send=2;
        cmd[0]=0;
    }
    else if(cmd[0]==en_enc_cmd)
    {
        attachInterrupt(0, step1, RISING);      //For encoders
        attachInterrupt(1, step2, RISING);
        cmd[0]=0;
    }
    else if(cmd[0]==dis_enc_cmd)
    {
        detachInterrupt(1);
        detachInterrupt(0);
        cmd[0]=0;
    }
    else if(cmd[0]==en_servo_cmd)
    {
        servo_flag=1;
        cmd[0]=0;
    }
    else if(cmd[0]==dis_servo_cmd)
    {
        servo_flag=0;
        cmd[0]=0;
    }
    else if(cmd[0]==en_com_timeout_cmd)//Encoder targetting
    {
        timeout=cmd[1]*256+cmd[2];
        cmd[0]=0;
        last_t=millis();
        timeout_f=1;
    }
    else if(cmd[0]==dis_com_timeout_cmd)//Encoder targetting
    {
        cmd[0]=0;
        last_t=millis();
        timeout_f=0;
        tgt_flag=0;
    }
    if(timeout_f)
    {
        if(millis()-last_t>timeout)
        {
          stp();
          cmd[0]=0;
          timeout_f=0;
        }
    }   
    if(cmd[0]==enc_tgt_cmd || tgt_flag==1)//Encoder targetting
    {
        if(cmd[0]==enc_tgt_cmd)
        {
            cmd[0]=0;
            tgt_flag=1;
            m1_en=cmd[1]/2;
            m2_en=cmd[1]%2;
            tgt=cmd[2]*256+cmd[3];
            e1=e2=0;
        }
        if(m1_en && !m2_en)
        {
            if(e1>=tgt)
            {
                cmd[0]=0;
                stp();
                tgt_flag=0;
            }
        }
        else if(!m1_en && m2_en)
        {
            if(e2>=tgt)
            {
                cmd[0]=0;
                stp();
                tgt_flag=0;
            }
        }
        else if(m1_en && m2_en)
        {
            if(e1>=tgt && e2>=tgt)
            {
                cmd[0]=0;
                stp();
                tgt_flag=0;
            }
        }
        if(debug)
        {
            Serial.print(cmd[1]);
            Serial.print(" ");
            Serial.print(cmd[2]);
            Serial.print(" ");
            Serial.print(cmd[3]);
            Serial.print(" ");
            Serial.print(e1);
            Serial.print(" ");
            Serial.print(e2);
            Serial.print(" ");
            Serial.print(bytes_to_send);
            Serial.print(" ");
            Serial.print(tgt_flag);
            Serial.print(" ");
            Serial.println(tgt);
        }
    }
    if(tgt_flag)//Set tgt_flag
      status_r|=1<<0;
    else
      status_r&=~(1<<0);
      
    if(timeout_f)//Set timeout_flag
      status_r|=1<<1;
    else
      status_r&=~(1<<1);
    if(servo_flag)  //Keep refreshing for software servo
        SoftwareServo::refresh();
}
//Recieve commands via I2C
void receiveData(int byteCount)
{
    while(Wire.available())
    {
        if(Wire.available()==4)
        {
            flag=0;
            index=0;
            if(timeout_f)
              last_t=millis();
        }
        cmd[index++] = Wire.read();
    }
}
// callback for sending data
volatile int ind=0;
void sendData()
{
    //if(timeout_f)
     //   last_t=millis();
    if(bytes_to_send==2)
    {
        Wire.write(payload[ind++]);
        if(ind==2)
        {
            ind=0;
            bytes_to_send=0;
        }
    }
    else// if(tgt_flag)
    {
        Wire.write(status_r);
    }
}
//Encoder ISR's
void step1()
{
    e1++;
    f1=1;
}
void step2()
{
    e2++;
    f2=1;
}
