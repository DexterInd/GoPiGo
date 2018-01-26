/*
 * #%L
 * **********************************************************************
 * ORGANIZATION  :  DexterIndustries
 * PROJECT       :  GoPiGo Java Library
 * FILENAME      :  Led.java
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

import com.dexterind.gopigo.utils.Debug;
import com.dexterind.gopigo.utils.Statuses;

/**
 * Handles the LED functions.
 * @author marcello
 *
 */
public class Led {
  /**
   * The left pin code.
   */
  private static final int LEFT_PIN_A = 10;
  /**
   * The right pin code.
   */
  private static final int RIGHT_PIN_A = 5;
  /**
   * The left pin code.
   */
  private static final int LEFT_PIN_B = 17;
  /**
   * The right pin code.
   */
  private static final int RIGHT_PIN_B = 16;
  /**
   * The left pin ID.
   */
  public static final int LEFT = 1;
  /**
   * The right pin ID.
   */
  public static final int RIGHT = 0;
  /**
   * The main object which handles the methods to get access to the resources
   * connected to the board.
   */
  private static Board board;
  /**
   * The current pin code.
   */
  private int pin = 0;
  /**
   * The current led id
   */
  private int id = 0;
  /**
   * The debug object.
   */
  private Debug debug;

  public Led(int id) {
    this.id = id;
  }

  /**
   * Sets the pin to use for the led.
   * @param pin The number of the pin where the led is attached.
   */
  public void setPin() {
    try {
      board = Board.getInstance();
      int vol = board.analogRead(7);
      int left_pin = 0;
      int right_pin = 0;
      if (vol > 700) {
        left_pin = LEFT_PIN_B;
        right_pin = RIGHT_PIN_B;
      } else {
        left_pin = LEFT_PIN_A;
        right_pin = RIGHT_PIN_A;
      }
      pin = id == LEFT ? left_pin : right_pin;
  } catch (IOException e) {
    e.printStackTrace();
  } catch (InterruptedException e) {
    e.printStackTrace();
  }
  }

  /**
   * Turns the led ON.
   * @return A status code.
   * @throws IOException
   */
  public int on() {
    if (pin == 0) {
      setPin();
    }
    try {
      board.setPinMode(pin, 1);
      return board.digitalWrite(pin, 1);
    } catch (IOException e) {
      e.printStackTrace();
      return Statuses.ERROR;
    }
  }

  /**
   * Turns the led OFF.
   * @return A status code.
   * @throws IOException
   */
  public int off() {
    if (pin == 0) {
      setPin();
    }
    try {
      board.setPinMode(pin, 1);
      return board.digitalWrite(pin, 0);
    } catch (IOException e) {
      e.printStackTrace();
      return Statuses.ERROR;
    }
  }
}