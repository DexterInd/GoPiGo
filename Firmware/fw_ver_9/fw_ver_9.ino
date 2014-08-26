///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Latest GoPiGo Firmware Source with I2C communication            
// http://www.dexterindustries.com/GoPiGo/                                                                
// History
// ------------------------------------------------
// Author     Date      		Comments
// Karan      21 Aug 14 		Initial Authoring
// Karan      25 Aug 14         Code clean-up and commenting		                                                         
// These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
// (http://creativecommons.org/licenses/by-sa/3.0/)           
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#include <Wire.h>           //For handling I2C
#include <SoftwareServo.h>  //Not using Servo.h because it disables timers
SoftwareServo servo1;

#define GOPIGO_ADDR 0x08    //GoPiGo Address 0x08

#define debug 1             //Make 0 to disable debugging

#define ver 9               //Firmware version (9 ->.9)

//Command list received from the Raspberry Pi
#define fwd_cmd         119     //Move forward with PID
#define motor_fwd_cmd   105     //Move forward without PID
#define bwd_cmd         115     //Move back with PID
#define motor_bwd_cmd   107     //Move back without PID
#define left_cmd        97      //Turn Left by turning off one motor
#define left_rot_cmd    98      //Rotate left by running both motors is opposite direction
#define right_cmd       100     //Turn Right by turning off one motor
#define right_rot_cmd   110     //Rotate Right by running both motors is opposite direction
#define stop_cmd        120     //Stop the GoPiGo
#define inc_speed_cmd   116     //Increase the speed by 10
#define dec_speed_cmd   103     //Decrease the speed by 10
#define volt_cmd        118     //Read the voltage of the batteries
#define us_cmd          117     //Read the distance from the ultrasonic sensor
#define led_cmd         108     //Turn On/Off the LED's
#define servo_cmd       101     //Rotate the servo
#define enc_tgt_cmd     50      //Set the encoder targeting
#define fw_ver_cmd      20      //Read the firmware version
#define en_enc_cmd      51      //Enable the encoders
#define dis_enc_cmd     52      //Disable the encoders
#define en_servo_cmd    61      //Enable the servo's
#define dis_servo_cmd   60      //Disable the servo's
#define set_r_speed_cmd 71      //Set the speed of the right motor
#define set_l_speed_cmd 70      //Set the speed of the left motor
#define enc_test        10      //Encoder Manufacturing test (not to be used by users)
#define serial_test     11      //Serial Port Manufacturing test (not to be used by users)
#define digital_write   12      //Digital write on a port
#define en_com_timeout_cmd  80  //Enable communication timeout
#define dis_com_timeout_cmd 81  //Disable communication timeout
#define timeout_status_cmd  82  //Read the timeout status

//Pin Definitions (Arduino Pin Definitions)
int motor1_control_pin1=7;      //Motor 1 direction control pins
int motor1_control_pin2=8;
int motor2_control_pin1=4;      //Motor 2 direction control pins
int motor2_control_pin2=13;
int motor1_speed_pin=9;         //Speed control pins
int motor2_speed_pin=6;

int spd=200,speed1,speed2;      //Speed control variables

int right_led_pin=5,left_led_pin=10;    //LED pins

int volt,led_pin,value;         //Voltage variables

int sf1=0,sf2=0,mf[2]= {0,0},td,cng_s;  //PID variables
float alpha=1,kp=1;
unsigned long ti1,tf1,ti2,tf2,td1,td2;

volatile int state = LOW;       //Encoder targeting variables
volatile int s=0;
volatile int f1=0,f2=0,e1=0,e2=0;
int tgt_flag=0,m1_en=0,m2_en=0,tgt=0;

volatile unsigned long last_t=0;
unsigned long timeout=0;
int timeout_f=0;

volatile int cmd[5],index=0,flag=0,bytes_to_send=0; //I2C Message variables
byte payload[3];

int servo_flag=0;       //Servo enabled or not

int status_r=0;

//MOTOR COMMANDS
//Standard logic from SN7544 motor driver

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
//  pow:    PWM power   (   0   - off
//                          255 - full power)
void led_light(int led_pin,int pow)
{
    if(led_pin==0)  //right led
    {
        analogWrite(right_led_pin,pow);
    }
    else            //left led
    {
        analogWrite(left_led_pin,pow);
    }
}

//Setting up the GoPiGo
void setup()
{
    if (debug)      //Enable the serial port on the GoPiGo
    {
        Serial.begin(115200);
        Serial.print("Ready");
    }
    
    attachInterrupt(0, step1, RISING);      //Attach the encoders to an ISR to keep track of the wheel rotations
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
//Main program loop
//IMPORTANT NOTE:   Set the cmd[0] to 0 to mark that the command has been executed 
//                  Be careful with this, because 

//FUNCTIONALITY NOTE:
//  *   servo::refresh() - takes .5 to 2.5 ms to complete
//  *   the motor interrupts have to be slower than the I2C interrupts. This has been a problem with I2C communication. The motor interrupts are of higher priority,
//      so if I2C block communication is used, there is a chance of the motors interrupting them. Conflicts can still be there but very rare
void loop()
{
    analogWrite(motor1_speed_pin,speed1);   //Write the speed to the motors
    analogWrite(motor2_speed_pin,speed2);
    
    //LED encoder test (Manufacturing test: Not to be used by user)
    //Blink the left LED when the right wheel is rotated and the right LED when the left wheel is rotated
    if(cmd[0]==enc_test)                
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
    
    //Serial test (Manufacturing test: Not to be used by user)
    //Waits for "a" to come on the serial bus and responds with a "k" and then closes the serial bus
    if(cmd[0]==serial_test)             
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
    
    //Digital Write
    //If "digital write" received via I2C, set the pin specified in cmd[1] to pin state specified in cmd[2]
    //e.g.:cmd[]=[12,7,1]
    //              12- digital_write
    //              7-  pin 7
    //              1-  High
    if(cmd[0]==digital_write)            
    {
        pinMode(cmd[1],OUTPUT);
        digitalWrite(cmd[1],cmd[2]);
    }
    
    //If moving forward or backward with PID
    if(cmd[0]==fwd_cmd || cmd[0]==bwd_cmd)  
    {
        //If encoder1 was hit (flag set using the ISR)
        if(f1==1)
        {
            //If this is the first reading, save the initial time and set that initial reading has been taken
            if(sf1==0)
            {
                sf1=1;
                ti1=micros();
            }
            //If this is the second reading, take the current time as the final time and find the time difference. This difference is the time taken for the wheel to move one encoder count
            //Also set a flag mf to indicate that one set of readings is over for motor1
            else
            {
                sf1=0;
                tf1=micros();
                td1=tf1-ti1;
                mf[0]=1;
            }
            //Wait for another encoder count to be hit
            f1=0;
        }
        //Do the same as above for encoder 2 too
        if(f2==1)
        {
            if(sf2==0)
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
        
        //Once we have the time taken by both the wheels to travel one encoder count, we can calculate the difference and find out which wheel is moving faster by how much.
        //the speed difference is compensated by increasing or decreasing the speed of wheel 2
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
                //FOR DEBUGGING PID CONTROL
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
    
    //Increase the speed
    if(cmd[0]==inc_speed_cmd) 
    {
        if(speed1>244)
            speed1=255;
        else
            speed1=speed1+10;
        speed2=speed1;
        cmd[0]=0;
    }
    
    //Decrease the speed
    else if(cmd[0]==dec_speed_cmd) 
    {
        if(speed1<11)
            speed1=0;
        else
            speed1=speed1-10;
        speed2=speed1;
        cmd[0] =0;
    }
    
    //Set speed of right motor
    if(cmd[0]==set_r_speed_cmd)
    {
      speed1=cmd[1];
      cmd[0]=0;
    }
    
    //Set speed of left motor
    else if(cmd[0]==set_l_speed_cmd)
    {
      speed2=cmd[1];
      cmd[0]=0;
    }

    //Set the motor controller to start moving forward. The speed is either constant with "nopid" or changing with "pid enabled"
    if(cmd[0]==fwd_cmd || cmd[0]==motor_fwd_cmd)
        forward();
        
    //Set the motor controller to turn left
    else if(cmd[0]==left_cmd)                        
        left();
        
    //Set the motor controller to rotate left
    else if(cmd[0]==left_rot_cmd)                  
        left_rot();
        
    //Set the motor controller to start moving backward. The speed is either constant wit "nopid" or changing with "pid enabled"
    else if(cmd[0]==bwd_cmd || cmd[0]==motor_bwd_cmd)   
        backward();
        
    //Set the motor controller to turn right
    else if(cmd[0]==right_cmd)                     
        right();
        
    //Set the motor controller to rotate right
    else if(cmd[0]==right_rot_cmd)                 
        right_rot();
        
    //Set the motor controller to stop
    else if(cmd[0]==stop_cmd)                      
        stp();
        
     //Read voltage and load the result into the I2C buffer
    else if(cmd[0]==volt_cmd)                      
    {
        volt=analogRead(0);
        payload[0]=volt/256;
        payload[1]=volt%256;
        bytes_to_send=2;
        cmd[0]=0;
    }
    
    //Read ultrasonic sensor and load the result into I2C buffer
    else if(cmd[0]==us_cmd) 
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
    
    //Turn on/off the LED
    //cmd[1]:   led_pin(0-right,1-left LED)
    //cmd[2]:   PWM power (0-255)
    else if(cmd[0]==led_cmd)
    {
        led_light(cmd[1],cmd[2]);
        cmd[0]=0;
    }
    
    //Set the servo angle  
    else if(cmd[0]==servo_cmd) 
    {
        value=cmd[1];
        if(debug)
        {
            Serial.println(value);
        }
        servo1.write(value);
        servo_flag=1;       //Set the servo flag so that it is refreshed every time in the main loop().
        cmd[0]=0;
    }
    
    //Load the firmware version in payload[] buffer to be sent back
    else if(cmd[0]==fw_ver_cmd)
    {
        payload[0]=ver;
        bytes_to_send=2;    //Enable this to send bytes back
        cmd[0]=0;
    }
    
    //If encoders are to be enabled, attach the interrupts to the pins
    else if(cmd[0]==en_enc_cmd)
    {
        attachInterrupt(0, step1, RISING);      
        attachInterrupt(1, step2, RISING);
        cmd[0]=0;
    }
    //To disable encoder interrupts, detach the interrupts
    else if(cmd[0]==dis_enc_cmd)
    {
        detachInterrupt(1);
        detachInterrupt(0);
        cmd[0]=0;
    }
    
    //Enable the servo
    else if(cmd[0]==en_servo_cmd)
    {
        servo_flag=1;
        cmd[0]=0;
    }
    
    //Disable the servo
    else if(cmd[0]==dis_servo_cmd)
    {
        servo_flag=0;
        cmd[0]=0;
    }
    
    //Set the communication timeout
    else if(cmd[0]==en_com_timeout_cmd)
    {
        timeout=cmd[1]*256+cmd[2];
        cmd[0]=0;
        last_t=millis();
        timeout_f=1;
    }
    
    //Disable the communication timeout
    else if(cmd[0]==dis_com_timeout_cmd)
    {
        cmd[0]=0;
        last_t=millis();
        timeout_f=0;
        tgt_flag=0;
    }
    
    //If timeout is enabled, check for timeout and if has occurred, stop the motors
    if(timeout_f)
    {
        if(millis()-last_t>timeout)
        {
          stp();
          cmd[0]=0;
          timeout_f=0;
        }
    }   
    
    //Encoder targeting function
    //Target unit in encoder counts. 18 counts per rotation
    if(cmd[0]==enc_tgt_cmd || tgt_flag==1)
    {
        //If the command to set the encoder targeting was just recieved
        if(cmd[0]==enc_tgt_cmd)
        {
            cmd[0]=0;
            tgt_flag=1;             //Enable the targeting flag
            m1_en=cmd[1]/2;         //Check if target on motor 1 set
            m2_en=cmd[1]%2;         //Check if target on motor 2 set
            tgt=cmd[2]*256+cmd[3];  //Set the target
            e1=e2=0;                //Set position of both the encoders to 0
        }
        //If only Motor 1 target is set
        if(m1_en && !m2_en)
        {
            if(e1>=tgt)     //Wait for encoder count to exceed the target, then stop
            {
                cmd[0]=0;
                stp();
                tgt_flag=0;
            }
        }
        //If only Motor 2 target is set
        else if(!m1_en && m2_en)
        {
            if(e2>=tgt)     //Wait for encoder count to exceed the target, then stop
            {
                cmd[0]=0;
                stp();
                tgt_flag=0;
            }
        }
        
        //If both Motor 1 and  Motor 2 targets are set
        else if(m1_en && m2_en)
        {
            if(e1>=tgt && e2>=tgt)  //Wait for encoder count on both to exceed the target, then stop
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
    
    //Refresh the flag status for the user to query 
    if(tgt_flag)//Set tgt_flag
        status_r|=1<<0;
    else
        status_r&=~(1<<0);
      
    if(timeout_f)//Set timeout_flag
        status_r|=1<<1;
    else
        status_r&=~(1<<1);
      
    //Keep refreshing software servo if servo's are being used
    if(servo_flag)  
        SoftwareServo::refresh();   // call this at least once every 50ms to keep the servos updated
}

//Receive commands via I2C
void receiveData(int byteCount)
{   
    while(Wire.available())
    {
        //When the buffer gets filled up with 4 bytes( the commands have to be 4 bytes in size), set the index back to 0 to read the next command
        if(Wire.available()==4)
        {
            flag=0;
            index=0;
            if(timeout_f)   //Refresh the communication time-out value
              last_t=millis();
        }
        cmd[index++] = Wire.read(); //Load the command into the buffer
    }
}

// callback for sending data
volatile int ind=0;
void sendData()
{
    //if(timeout_f)
     //   last_t=millis();
    //Sends 2 bytes back for the Ultrasonic read, voltage and firmware version
    if(bytes_to_send==2)
    {
        Wire.write(payload[ind++]);
        if(ind==2)
        {
            ind=0;
            bytes_to_send=0;
        }
    }
    else// Send back the status flag
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
