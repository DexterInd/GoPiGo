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
package com.dexterind.gopigo.behaviours;

import java.io.IOException;
import java.util.*;

import com.dexterind.gopigo.components.*;
import com.dexterind.gopigo.utils.*;

/**
 * Handles all the methods related to the movement of the GoPigo.
 * @author marcello
 *
 */
public class Motion {
  /**
   * The main object which handles the methods to get access to the resources
   * connected to the board.
   */
  private static Board board;
  /**
   * The instance of the current object.
   */
  private static Motion instance = null;
  /**
   * The HashMap of the directions. It could be useful as helper for rotating the
   * servo motor or the GoPiGo itself.
   */
  public Map<String, Integer> directions = new HashMap<String, Integer>();
  /**
   * The debug object.
   */
  private Debug debug;

  public Motion() throws IOException, InterruptedException {
    directions.put("n", 0);
    directions.put("ne", 45);
    directions.put("e", 90);
    directions.put("se", 135);
    directions.put("s", 180);
    directions.put("sw", 225);
    directions.put("w", 270);
    directions.put("nw", 315);

    board = Board.getInstance();
  }

  /**
   * Provides a global point of access to the Motion instance.
   * @return  the <code>Motion</code> instance.
   */
  public static Motion getInstance() throws IOException, InterruptedException {
    if(instance == null) {
      instance = new Motion();
    }
    return instance;
  }

  /**
   * Moves forward the Gopigo.
   * @param usePid A boolean flag which defines if it's needed to use or not the PID.
   * @return A status code.
   * @throws IOException
   */
  public int forward(boolean usePid) throws IOException {
    int command = usePid ? Commands.FWD : Commands.MOTOR_FWD;
    return board.writeI2c(command, Commands.UNUSED, Commands.UNUSED, Commands.UNUSED);
  }

  /**
   * Moves backward the Gopigo.
   * @param usePid A boolean flag which defines if it's needed to use or not the PID.
   * @return A status code.
   * @throws IOException
   */
  public int backward(boolean usePid) throws IOException {
    int command = usePid ? Commands.BWD : Commands.MOTOR_BWD;
    return board.writeI2c(command, Commands.UNUSED, Commands.UNUSED, Commands.UNUSED);
  }

  /**
   * Moves the Gopigo to the left.
   * @return A status code.
   * @throws IOException
   */
  public int left() throws IOException {
    return board.writeI2c(Commands.LEFT, Commands.UNUSED, Commands.UNUSED, Commands.UNUSED);
  }

  /**
   * Rotates the Gopigo to the left.
   * @return A status code.
   * @throws IOException
   */
  public int leftWithRotation() throws IOException {
    return board.writeI2c(Commands.LEFT_ROT, Commands.UNUSED, Commands.UNUSED, Commands.UNUSED);
  }

  /**
   *  Moves the Gopigo to the right.
   * @return A status code.
   * @throws IOException
   */
  public int right() throws IOException {
    return board.writeI2c(Commands.RIGHT, Commands.UNUSED, Commands.UNUSED, Commands.UNUSED);
  }

  /**
   * Rotates the Gopigo to the right.
   *
   * @return A status code.
   * @throws IOException
   */
  public int rightWithRotation() throws IOException {
    return board.writeI2c(Commands.RIGHT_ROT, Commands.UNUSED, Commands.UNUSED, Commands.UNUSED);
  }

  /**
   * Stops any kind of movement.
   * @return A status code.
   * @throws IOException
   */
  public int stop() throws IOException {
    return board.writeI2c(Commands.STOP, Commands.UNUSED, Commands.UNUSED, Commands.UNUSED);
  }

  /**
   * Increases the speed of both the motors.
   *
   * @return A status code.
   * @throws IOException
   */
  public int increaseSpeed() throws IOException {
    return board.writeI2c(Commands.ISPD, Commands.UNUSED, Commands.UNUSED, Commands.UNUSED);
  }

  /**
   * Decreases the speed of both the motors.
   * @return A status code.
   * @throws IOException
   */
  public int decreaseSpeed() throws IOException {
    return board.writeI2c(Commands.DSPD, Commands.UNUSED, Commands.UNUSED, Commands.UNUSED);
  }

  /**
   * Sets the speed only for the left motor.
   * @param speed A speed value between 0 and 255
   * @return A status code.
   * @throws IOException
   */
  public int setLeftSpeed(int speed) throws IOException {
    if (speed > 255) {
      speed = 255;
    } else if (speed < 0) {
      speed = 0;
    }

    return board.writeI2c(Commands.SET_LEFT_SPEED, speed, Commands.UNUSED, Commands.UNUSED);
  }

  /**
   * Sets the speed only for the right motor.
   * @param speed A speed value between 0 and 255.
   * @return A status code.
   * @throws IOException
   */
  public int setRightSpeed(int speed) throws IOException {
    if (speed > 255) {
      speed = 255;
    } else if (speed < 0) {
      speed = 0;
    }

    return board.writeI2c(Commands.SET_RIGHT_SPEED, speed, Commands.UNUSED, Commands.UNUSED);
  }

  /**
   * Sets the speed for both the motors.
   * @param speed A speed value between 0 and 255
   * @return A status code.
   * @throws IOException
   */
  public int setSpeed(int speed) throws IOException {
    if (speed > 255) {
      speed = 255;
    } else if (speed < 0) {
      speed = 0;
    }

    setLeftSpeed(speed);
    setRightSpeed(speed);

    return Statuses.OK;
  }

  /**
   * Executes a Trim test.
   * @param value The value to test between -100 and 100.
   * @return A status code.
   * @throws IOException
   */
  public double trimTest(int value) throws IOException {
    if (value > 100) {
      value = 100;
    } else if (value < -100) {
      value = -100;
    }
    value +=100;

    return board.writeI2c(Commands.TRIM_TEST, value, Commands.UNUSED, Commands.UNUSED);
  }

  /**
   * Reads the current Trim value.
   * @return The current Trim value between -100 and 100.
   * @throws IOException
   */
  public double trimRead() throws IOException {
    board.writeI2c(Commands.TRIM_READ, Commands.UNUSED, Commands.UNUSED, Commands.UNUSED);
    board.sleep(80);

    byte[] b1 = board.readI2c(1);
    byte[] b2 = board.readI2c(1);
    int val1 = (int)b1[0] & 0xFF;
    int val2 = (int)b2[0] & 0xFF;

    if (val1 != -1 && val2 != -1) {
      int v = val1 * 256 + val2;
      if (v == 255) {
        return -3;
      }
      return v;
    } else {
      return Statuses.ERROR;
    }
  }

  /**
   * Sets the Trim value.
   * @param value The Trim value between -100 and 100.
   * @return A status code.
   * @throws IOException
   */
  public double trimWrite(int value) throws IOException {
    if (value > 100) {
      value = 100;
    } else if (value < -100) {
      value = -100;
    }
    value +=100;

    return board.writeI2c(Commands.TRIM_WRITE, value, Commands.UNUSED, Commands.UNUSED);
  }

 /**
  * Reads the timeout status.
  * @return The timeout value.
  * @throws IOException
  */
  public int readTimeoutStatus() throws IOException {
    int[] status = board.readStatus();
    return status[1];
  }

  /**
   * Enables the communication timeout.
   * @param timeout The value of the timout.
   * @return A status code.
   * @throws IOException
   */
  public int enableCommunicationTimeout(int timeout) throws IOException {
    return board.writeI2c(Commands.EN_COM_TIMEOUT, timeout / 256, timeout % 256, Commands.UNUSED);
  }

  /**
   * Disables the communication timeout.
   * @return A status code.
   * @throws IOException
   */
  public int disableCommunicationTimeout() throws IOException {
    return board.writeI2c(Commands.DIS_COM_TIMEOUT, Commands.UNUSED, Commands.UNUSED, Commands.UNUSED);
  }
}