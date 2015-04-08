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
package com.dexterind.gopigo.components;

import java.io.IOException;

import com.dexterind.gopigo.utils.*;

/**
 * Implements the methods needed to set, read, enable or disable the encoders.
 * @author marcello
 *
 */
public class Encoders {
  /**
   * The main object which handles the methods to get access to the resources
   * connected to the board.
   */
  private static Board board;
  /**
   * The instance of the current object.
   */
  private static Encoders instance = null;
  /**
   * The debug object.
   */
  private Debug debug;

  public Encoders() throws IOException, InterruptedException {
    board = Board.getInstance();
  }

  /**
   * Provides a global point of access to the Encoders instance.
   * @return  the <code>Encoders</code> instance.
   */
  public static Encoders getInstance() throws IOException, InterruptedException {
    if(instance == null) {
      instance = new Encoders();
    }
    return instance;
  }

  /**
   * Sets the targeting for both the motors.
   * @param m1 The value for the motor 1.
   * @param m2 The value for the motor 2.
   * @param target TODO: Find a nice description for the target
   * @return A status code.
   * @throws IOException
   */
  public int targeting(int m1, int m2, int target) throws IOException {
    if (m1 > 1 || m1 < 0 || m2 > 1 || m2 < 0) {
      return Statuses.ERROR;
    }
    int m_sel = m1 * 2 + m2;
    return board.writeI2c(Commands.ENC_TGT, m_sel, target / 256, target % 256);
  }

  /**
   * Reads the encoding value for the motor.
   * @param motor The motor id to read.
   * @return The value for the motor or a "error" status code in case of failure.
   * @throws IOException
   */
  public int read(int motor) throws IOException {
    board.writeI2c(Commands.ENC_READ, motor, Commands.UNUSED, Commands.UNUSED);
    board.sleep(80);

    byte[] b1 = board.readI2c(1);
    byte[] b2 = board.readI2c(1);
    int val1 = (int)b1[0] & 0xFF;
    int val2 = (int)b2[0] & 0xFF;

    if (val1 != -1 && val2 != -1) {
      int v = val1 * 256 + val2;
      return v;
    } else {
      return Statuses.ERROR;
    }
  }

  /**
   * Reads the encoders status.
   * @return The encoders status
   * @throws IOException
   */
  public int readStatus() throws IOException {
    int[] status = board.readStatus();
    return status[0];
  }

  /**
   * Enables the encoders.
   * @return A status code.
   * @throws IOException
   */
  public int enable() throws IOException {
    return board.writeI2c(Commands.EN_ENC, Commands.UNUSED, Commands.UNUSED, Commands.UNUSED);
  }

  /**
   * Disables the encoders.
   * @return A status code.
   * @throws IOException
   */
  public int disable() throws IOException {
    return board.writeI2c(Commands.DIS_ENC, Commands.UNUSED, Commands.UNUSED, Commands.UNUSED);
  }
}