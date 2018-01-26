/*
 * #%L
 * **********************************************************************
 * ORGANIZATION  :  DexterIndustries
 * PROJECT       :  GoPiGo Java Library
 * FILENAME      :  Encoders.java
 * AUTHOR        :  Marcello Barile <marcello.barile@gmail.com>
 *
 * This file is part of the GoPiGo Java Library project. More information about
 * this project can be found here:  https://github.com/DexterInd/GoPiGo
 * **********************************************************************
 * %%
 * GoPiGo for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
 * Copyright (C) 2017  Dexter Industries

 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.

 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.

 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
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