/*
 * #%L
 * **********************************************************************
 * ORGANIZATION  :  DexterIndustries
 * PROJECT       :  GoPiGo Java Library
 * FILENAME      :  Servo.java
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
 * It allows to move, enable or disable the servo motor.
 * @author marcello
 *
 */
public class Servo {
  /**
   * The main object which handles the methods to get access to the resources
   * connected to the board.
   */
  private static Board board;
  /**
   * The instance of the current object.
   */
  private static Servo instance = null;
  /**
   * The current position value
   */
  private int position = -1;
  /**
   * The debug object.
   */
  private Debug debug;

  public Servo() throws IOException, InterruptedException {
    board = Board.getInstance();
  }

  /**
   * Provides a global point of access to the Servo instance.
   * @return  the <code>Servo</code> instance.
   */
  public static Servo getInstance() throws IOException, InterruptedException {
    if(instance == null) {
      instance = new Servo();
    }
    return instance;
  }

  /**
   * Moves the servo motor to the position.
   * @param position The value of the rotation in degrees.
   * @return A status code.
   * @throws IOException
   */
  public int move(int position) throws IOException {
    this.position = position;
    return board.writeI2c(Commands.SERVO, position, Commands.UNUSED, Commands.UNUSED);
  }

  /**
   * Enables the servo motor.
   * @return A status code.
   * @throws IOException
   */
  public int enable() throws IOException {
    return board.writeI2c(Commands.EN_SERVO, Commands.UNUSED, Commands.UNUSED, Commands.UNUSED);
  }

  /**
   * Disables the servo motor.
   * @return A status code.
   * @throws IOException
   */
  public int disable() throws IOException {
    return board.writeI2c(Commands.DIS_SERVO, Commands.UNUSED, Commands.UNUSED, Commands.UNUSED);
  }
}