/*
 * #%L
 * **********************************************************************
 * ORGANIZATION  :  DexterIndustries
 * PROJECT       :  GoPiGo Java Library
 * FILENAME      :  Gopigo.java
 * AUTHOR        :  Marcello Barile <marcello.barile@gmail.com>
 *
 * This file is part of the GoPiGo Java Library project. More information about
 * this project can be found here:  https://github.com/DexterInd/GoPiGo
 * **********************************************************************
 * %%
 * This project is open source. These files have been made available
 * online through a Creative Commons Attribution-ShareAlike 3.0 license.
 *
 *      http://creativecommons.org/licenses/by-sa/3.0/
 *
 * #L%
 */
package com.dexterind.gopigo.utils;

public class Commands {
  /**
   * Move forward with PID.
   */
  public static final int FWD                  = 119;
  /**
   * Move forward without PID.
   */
  public static final int MOTOR_FWD            = 105;
  /**
   * Move backward with PID.
   */
  public static final int BWD                  = 115;
  /**
   * Move backward without PID.
   */
  public static final int MOTOR_BWD            = 107;
  /**
   * Turn left by turning off one motor.
   */
  public static final int LEFT                 = 97;
  /**
   * Rotate left by running both motors in opposite direction.
   */
  public static final int LEFT_ROT             = 98;
  /**
   * Turn right by turning off one motor.
   */
  public static final int RIGHT                = 100;
  /**
   * Rotate right by running both motors in opposite direction.
   */
  public static final int RIGHT_ROT            = 110;
  /**
   * Stop the GoPiGo.
   */
  public static final int STOP                 = 120;
  /**
   * Increase the speed by 10.
   */
  public static final int ISPD                 = 116;
  /**
   * Decrease the speed by 10.
   */
  public static final int DSPD                 = 103;
  /**
   * Control motor1.
   */
  public static final int M1                   = 111;
  /**
   * Control motor2.
   */
  public static final int M2                   = 112;
  /**
   * Read the voltage of the batteries.
   */
  public static final int VOLT                 = 118;
  /**
   * Read the distance from the ultrasonic sensor.
   */
  public static final int US                   = 117;
  /**
   * Turn ON/OFF the LEDs.
   */
  public static final int LED                  = 108;
  /**
   * Rotate the servo.
   */
  public static final int SERVO                = 101;
  /**
   * Set the encoder targeting.
   */
  public static final int ENC_TGT              = 50;
  /**
   * Read the firmware version.
   */
  public static final int FW_VER               = 20;
  /**
   * Enable the encoders.
   */
  public static final int EN_ENC               = 51;
  /**
   * Disable the encoders.
   */
  public static final int DIS_ENC              = 52;
  /**
   * Read the encoder status.
   */
  public static final int READ_ENC_STATUS      = 53;
  /**
   * Enable the servo.
   */
  public static final int EN_SERVO             = 61;
  /**
   * Disable the servo.
   */
  public static final int DIS_SERVO            = 60;
  /**
   * Set the speed of the right motor.
   */
  public static final int SET_LEFT_SPEED       = 70;
  /**
   * Set the speed of the left motor.
   */
  public static final int SET_RIGHT_SPEED      = 71;
  /**
   * Enable the communication timeout.
   */
  public static final int EN_COM_TIMEOUT       = 80;
  /**
   * Disable the communication timeout.
   */
  public static final int DIS_COM_TIMEOUT      = 81;
  /**
   * Read the timeout status.
   */
  public static final int TIMEOUT_STATUS       = 82;
  /**
   * Read the encoder values.
   */
  public static final int ENC_READ             = 53;
  /**
   * Test the trim values.
   */
  public static final int TRIM_TEST            = 30;
  /**
   * Write the trim values.
   */
  public static final int TRIM_WRITE           = 31;
  /**
   * Read the trim values.
   */
  public static final int TRIM_READ            = 32;
  /**
   * Digital write on a port.
   */
  public static final int DIGITAL_WRITE        = 12;
  /**
   * Digital read on a port.
   */
  public static final int DIGITAL_READ         = 13;
  /**
   * Analog read on a port.
   */
  public static final int ANALOG_READ          = 14;
  /**
   * Analog read on a port.
   */
  public static final int ANALOG_WRITE         = 15;
  /**
   * Set up the pin mode on a port.
   */
  public static final int PIN_MODE             = 16;

  /**
   * This allows us to be more specific about which commands contain unused ints
   */
  public static final int UNUSED               = 0;

  public Commands(){}
}