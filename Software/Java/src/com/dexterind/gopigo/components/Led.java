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

import com.dexterind.gopigo.utils.Debug;

/**
 * Handles the LED functions.
 * @author marcello
 *
 */
public class Led {
  /**
   * The left pin code.
   */
  private static final int LEFT_PIN = 10;
  /**
   * The right pin code.
   */
  private static final int RIGHT_PIN = 5;
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
   * The debug object.
   */
  private Debug debug;

  public Led(int id) throws IOException, InterruptedException {
    pin = id == LEFT ? LEFT_PIN : RIGHT_PIN;
    board = Board.getInstance();
  }

  /**
   * Turns the led ON.
   * @return A status code.
   * @throws IOException
   */
  public int on() throws IOException {
    return board.digitalWrite(pin, 1);
  }

  /**
   * Turns the led OFF.
   * @return A status code.
   * @throws IOException
   */
  public int off() throws IOException {
    return board.digitalWrite(pin, 0);
  }
}