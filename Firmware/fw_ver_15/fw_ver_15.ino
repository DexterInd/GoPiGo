///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Latest GoPiGo Firmware Source with I2C communication            
// http://www.dexterindustries.com/GoPiGo/                                                                
// History
// ------------------------------------------------
// Author     Date      		Comments
// Karan      21 Aug 14 		Initial Authoring
// Karan      25 Aug 14         Code clean-up and commenting
// John       25 Sep 14         Changes for div8 fuse settings.	
// Karan      01 June 15        Changes for v16 and IR control added
//	                                                         
// These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
// (http://creativecommons.org/licenses/by-sa/3.0/)            
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//  Fuse Settings:
//  Extended - 0xFD
//  High     - 0xDA
//  Low      - 0x7F
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Clock Settings:
// The clock is reduced by 8 by setting the div8 fuse.  Use this as a reference:  http://playground.arduino.cc/Learning/Atmega83-3V
// We made this change to decrease noise from the motors.
// We have to lower the F_CPU settings.
// In the file: \Arduino\hardware\arduino\boards.txt 
// Change, on line 16 under "Arduino Uno": 
//     uno.build.f_cpu=16000000L
// to:
//     uno.build.f_cpu=2000000L
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#include <avr/power.h>
#include <Wire.h>           //For handling I2C
#include "SoftwareServo.h"  //Not using Servo.h because it disables timers
#include <EEPROM.h>
// #include "IRSendRev.h"

SoftwareServo servo1;

#define GOPIGO_ADDR 0x08    //GoPiGo Address 0x08

#define debug 0             //Make 0 to disable debugging

#define ver 15              //Firmware version (10 ->1.0)

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
#define m1_cmd          111     //Control motor1
#define m2_cmd          112     //Control motor2
# define read_motor_speed_cmd   114     //Read the motor speeds

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

#define enc_read        53      //Read the encoder value for motors
 
#define trim_test       30      //Test the trim value for a motor
#define trim_write      31      //Write the trim value to eeprom for motor m2
#define trim_read       32      //Read the trim value from eeprom

#define en_com_timeout_cmd  80  //Enable communication timeout
#define dis_com_timeout_cmd 81  //Disable communication timeout
#define timeout_status_cmd  82  //Read the timeout status

#define digital_write   12      //Digital write on a port
#define digital_read    13      //Digital read on a port
#define analog_read     14      //Analog read on a port
#define analog_write    15      //Analog read on a port
#define pin_mode        16      //Set up the pin mode on a port

#define ep_sig1         0xDE
#define ep_sig2         0x14

#define ir_init_cmd		22
#define ir_read_cmd		21

//MAKE COMPATIBLE WITH OLD FIRMWARE
//Pin Definitions (Arduino Pin Definitions)
int motor1_control_pin1=7;      //Motor 1 direction control pins
int motor1_control_pin2=8;
int motor2_control_pin1=4;      //Motor 2 direction control pins
int motor2_control_pin2=14;
int motor1_speed_pin=9;         //Speed control pins
int motor2_speed_pin=6;

int spd=200,speed1,speed2,temp_speed2;      //Speed control variables
int pid_flag=0;
int right_led_pin=16,left_led_pin=17;    //LED pins

int volt,led_pin,value;         //Voltage variables

int sf1=0,sf2=0,mf[2]= {0,0},cng_s;  //PID variables
float alpha=1,kp=1;
unsigned long ti1,tf1,ti2,tf2,td1,td2;
long td;

volatile int state = LOW;       //Encoder targeting variables
volatile int s=0;
volatile int f1=0,f2=0,e1=0,e2=0;
int tgt_flag=0,m1_en=0,m2_en=0,tgt=0;

volatile unsigned long last_t=0;
unsigned long timeout=0;
int timeout_f=0;

volatile int cmd[5],index=0,bytes_to_send=0; //I2C Message variables
byte payload[21];
unsigned char dta[20];
int length;
int temp,i;

int servo_flag=0;       //Servo enabled or not
unsigned long time_since_servo_cmd=0;
int status_r=0;

int trim_val=0,speed2_trim=0;
byte ep1,ep2,ep3;
//MOTOR COMMANDS
//Standard logic from SN7544 motor driver

//Motor1 individual control
//  direction:  1- Forward
//              0- Backward
//  speed:  pwm speed from 0 to 255

void motor1_control(int direction, int speed)
{
    speed1=speed;
    if(direction)
    {
        digitalWrite(motor1_control_pin1, LOW);
        digitalWrite(motor1_control_pin2, HIGH);
    }
    else if(direction==0)
    {
        digitalWrite(motor1_control_pin1, HIGH);
        digitalWrite(motor1_control_pin2, LOW);
    }
}

//Motor2 individual control
//  direction:  1- Forward
//              0- Backward
//  speed:  pwm speed from 0 to 255

void motor2_control(int direction, int speed)
{
    speed2=speed;
    if(direction)
    {
        digitalWrite(motor2_control_pin1, LOW);
        digitalWrite(motor2_control_pin2, HIGH);
    }
    else if(direction==0)
    {
        digitalWrite(motor2_control_pin1, HIGH);
        digitalWrite(motor2_control_pin2, LOW);
    }
}

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
//  state:  0 - off
//          1 - on)
void led_light(int led_pin,int state)
{
    if(led_pin==0)  //right led
    {
        digitalWrite(right_led_pin,state);
    }
    else            //left led
    {
        digitalWrite(left_led_pin,state);
    }
}

//Setting up the GoPiGo
void setup()
{

    if (debug)      //Enable the serial port on the GoPiGo
    {
        Serial.begin(19200);
        Serial.print("Ready");
    }

    attachInterrupt(0, step1, RISING);      //Attach the encoders to an ISR to keep track of the wheel rotations
    attachInterrupt(1, step2, RISING);
    
    pinMode(motor1_control_pin1, OUTPUT);   //Attach motor direction control pins
    pinMode(motor1_control_pin2, OUTPUT);
    pinMode(motor2_control_pin1, OUTPUT);
    pinMode(motor2_control_pin2, OUTPUT);
    // pinMode(left_led_pin, OUTPUT);   //Attach motor direction control pins
    // pinMode(right_led_pin, OUTPUT);
    
    servo1.attach(5);                       //Set up the Servo
    //servo1.setMaximumPulse(3000);
    
    Wire.begin(GOPIGO_ADDR);                //Set up I2C
    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);
    
    speed1=speed2=spd;
    
    //IR.Init(A1);
    //Load the trim value for motor 2 from the EEPROM
    ep1=EEPROM.read(0);
    ep2=EEPROM.read(1);
    ep3=EEPROM.read(2);
    //Load the trim value of the first 2 bytes are the right signature
    if (ep1==ep_sig1 && ep2==ep_sig2)
        trim_val=ep3;
    //Disable trim if the signature is not a match
    else    
        trim_val=100; 
         
    // digitalWrite(right_led_pin,HIGH);
    // digitalWrite(left_led_pin,HIGH);
    // delay(1000);
    // digitalWrite(right_led_pin,LOW);
    // digitalWrite(left_led_pin,LOW);
}
//Main program loop
//IMPORTANT NOTE:   Set the cmd[0] to 0 to mark that the command has been executed 
//                  Be careful with this, because for some commands like fwd() and bwd() you'll not want the motors to stop when the GoPiGo receives any command. So most of the commands are run only once but when commands like fwd() , bwd() are running, cmd[0] goes back to the old state after the new commands are successfully run.

//FUNCTIONALITY NOTE:
//  *   servo::refresh() - takes .5 to 2.5 ms to complete
//  *   the motor interrupts have to be slower than the I2C interrupts. This has been a problem with I2C communication. The motor interrupts are of higher priority,
//      so if I2C block communication is used, there is a chance of the motors interrupting them. Conflicts can still be there but very rare
void loop()
{
    //Update the speed by taking in account the trim value
    speed2_trim=int(speed2+(speed2*float(trim_val-100)/100));
    if (speed2_trim>255)
        speed2_trim=255;
    else if(speed2_trim<0)
        speed2_trim=0;
        
    analogWrite(motor1_speed_pin,speed1);   //Write the speed to the motors
    analogWrite(motor2_speed_pin,speed2_trim);
    
    //LED encoder test (Manufacturing test: Not to be used by user)
    //Blink the left LED when the right wheel is rotated and the right LED when the left wheel is rotated
    if(cmd[0]==enc_test)                
    {
        if(f1==1)
        {
            led_light(0,1);
            f1=0;
        }
        if(f2==1)
        {
            led_light(1,1);
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
        cmd[0]=0;
    }
    
    //Digital Read
    //If "digital read" received via I2C, read the pin specified in cmd[1] 
    //e.g.:cmd[]=[13,7]
    //              13- digital_read
    //              7-  pin 7
    if(cmd[0]==digital_read)            
    {
        pinMode(cmd[1],INPUT);
        payload[0]=digitalRead(cmd[1]);
        payload[1]=0;
        bytes_to_send=2;    //Enable this to send bytes back
        cmd[0]=0;

    }
    
    //Analog Read
    //If "analog read" received via I2C, read the pin specified in cmd[1] and save the data in payload
    //e.g.:cmd[]=[14,7]
    //              14- analog_read
    //              7-  pin 7
    if(cmd[0]==analog_read)            
    {
        temp=analogRead(cmd[1]);
        payload[0]=temp/256;
        payload[1]=temp%256;
        bytes_to_send=2;    //Enable this to send bytes back
        cmd[0]=0;
    }
    
    //Analog Write
    //If "analog write" received via I2C, write the analog value specified by cmd[2] to the pin specified in cmd[1]
    //e.g.:cmd[]=[15,7,127]
    //              14- analog_read
    //              7-  pin 7
    //              127- value to write
    if(cmd[0]==analog_write)            
    {
        analogWrite(cmd[1],cmd[2]);
        cmd[0]=0;
    }
    
    //Pin Mode
    //If "pin mode" received via I2C, set the pin specified in cmd[1] to pin state specified in cmd[2]
    //      State: 0 - Input
    //      State: 1 - Output
    //e.g.:cmd[]=[16,7,1]
    //              16- pin_mode
    //              7-  pin 7
    //              1-  Output
    if(cmd[0]==pin_mode)            
    {
        if(cmd[2]==0)
            pinMode(cmd[1],INPUT);
        else if(cmd[2]==1)
            pinMode(cmd[1],OUTPUT);
        cmd[0]=0;
    }
    
    //If moving forward or backward with PID
    if(cmd[0]==fwd_cmd || cmd[0]==bwd_cmd)  
    {
        //if going to some other command other than PID control, then save tehe speed to revert back to it later
        if (pid_flag==0)
        {
            temp_speed2=speed2;
            pid_flag=1;
        }
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
        /*Serial.print("~~~~~~~~~~");
        Serial.print("tdiff1: ");
        Serial.println(td1);
        Serial.print("tdiff2: ");
        Serial.println(td2);
        Serial.print("mf0: ");
        Serial.println(mf[0]);
        Serial.print("mf1: ");
        Serial.println(mf[1]);*/
        if(mf[1]==1)// || mf[1]==1)
        {
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
                if(debug)
                {
                Serial.print("tdiff1: ");
                Serial.println(td1);
                Serial.print("tdiff2: ");
                Serial.println(td2);
                Serial.print("tdiff: ");
                Serial.println(td);
                Serial.print("alpha: ");
                Serial.println(alpha);
                Serial.print("s1 ");
                Serial.print(speed1);
                Serial.print(" s2 ");
                Serial.print(speed2);
                Serial.print(" cng_s ");
                Serial.println(cng_s);
                Serial.println("");
                }
            }
        }
    }
    else
    {
        //if going to some other command other than PID control, then revert the speed back to the original speed
        if(pid_flag)
        {
            speed2=temp_speed2;
            pid_flag=0;
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
    
    //Set motor1 movement
    else if(cmd[0]==m1_cmd)
        motor1_control(cmd[1],cmd[2]);
        
    //Set motor2 movement
    else if(cmd[0]==m2_cmd)
        motor2_control(cmd[1],cmd[2]);
        
    //Read voltage and load the result into the I2C buffer
    else if(cmd[0]==volt_cmd)                      
    {
        //MAKE COMPATIBLE WITH OLD FIRMWARE
        // volt=analogRead(0);
        volt=analogRead(6);
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
    
    else if(cmd[0]==read_motor_speed_cmd) 
    {
        payload[0]=speed1;
        payload[1]=speed2;
        bytes_to_send=2;
        cmd[0]=0;
    }
    else if(cmd[0]==ir_init_cmd) 
    {
        // Serial.println("11");
        // Serial.println(cmd[1]);
        //IR.Init(cmd[1]);
        cmd[0]=0;
    }
    else if(cmd[0]==ir_read_cmd) 
    {
        //Serial.println("21");
        // if(IR.IsDta())
        // {
            // Serial.println("33");
            // int length= IR.Recv(dta);
             // for(int i=0;i<20;i++)
                // {
                  // Serial.print(dta[i]);
                  // Serial.print(",");
                // }
            Serial.println(" ");
            // payload[0]=1;
            // for(i=0;i<20;i++)
                // payload[i+1]=dta[i];
            // bytes_to_send=21;
        //}
        cmd[0]=0;
    }
    //Turn on/off the LED
    //cmd[1]:   led_pin(0-right,1-left LED)
    //cmd[2]:   state (0,1)
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
        time_since_servo_cmd=millis();
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
            cmd[0]=0;               //Command has been read
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
                cmd[0]=0;   //This should not disrupt other functions because the forward nad back commands would be running in normal operation
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
      
    //Encoder read
    //If "enc_read" received via I2C, read the encoder value for motor in cmd[1] for and send the data in payload
    //e.g.: cmd[]=[1]
    //      0- motor1
    //      1- motor2
    if(cmd[0]==enc_read)            
    {
        if(cmd[1]==0)
            temp=e1;
        else
            temp=e2;
        payload[0]=temp/256;
        payload[1]=temp%256;
        bytes_to_send=2;    //Enable this to send bytes back
        cmd[0]=0;
    }
    
    //Test a trim value for motor2 temporarily
    //cmd[1]:   value from 0 to 200 for the range -100 to 100 for % change in the motor 2 speed
    if(cmd[0]==trim_test)
    {
        trim_val=cmd[1];
        cmd[0]=0;
    }
    
    //Read the trim value in EEPROM
    //returns -1 if nothing is available
    if(cmd[0]==trim_read)
    {
        ep1=EEPROM.read(0);
        ep2=EEPROM.read(1);
        ep3=EEPROM.read(2);
        if (ep1==ep_sig1 && ep2==ep_sig2)
            temp=ep3;
        else    
            temp=-1;
        payload[0]=temp/256;
        payload[1]=temp%256;
        bytes_to_send=2;    //Enable this to send bytes back
        cmd[0]=0;
    }
    
    //Write the trim value with the signature in the EEPROM
    if(cmd[0]==trim_write)
    {
        trim_val=cmd[1];
        EEPROM.write(0,ep_sig1);
        EEPROM.write(1,ep_sig2);
        EEPROM.write(2,trim_val);
        cmd[0]=0;
    }
    //Keep refreshing software servo if servo's are being used
    if(servo_flag)  
        SoftwareServo::refresh();   // call this at least once every 50ms to keep the servos updated
    
    //Turn off servo refresh to avoid fuzzing after 10 seconds since the last command
    if(millis()-time_since_servo_cmd>10000)
        servo_flag=0;
}

//Receive commands via I2C
void receiveData(int byteCount)
{   
    while(Wire.available())
    {
        //When the buffer gets filled up with 4 bytes( the commands have to be 4 bytes in size), set the index back to 0 to read the next command
        if(Wire.available()==4)
        {
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
    else if(bytes_to_send==20)
    {
        Wire.write(payload,20);
		bytes_to_send=0;
    } 
    else if(bytes_to_send==21)
    {
        Wire.write(payload[ind++]);
        if(ind==21)
        {
            ind=0;
            bytes_to_send=0;
            payload[0]=0;
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
