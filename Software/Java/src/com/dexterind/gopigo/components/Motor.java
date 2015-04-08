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

import com.dexterind.gopigo.utils.Commands;
import com.dexterind.gopigo.utils.Debug;

/**
 * Handles the motor functions.
 * @author marcello
 *
 */
public class Motor {
  /**
   * The left motor command.
   */
  private static final int LEFT_COMMAND = Commands.M2;
  /**
   * The right motor command.
   */
  private static final int RIGHT_COMMAND = Commands.M1;
  /**
   * The forward command.
   */
  public static final int FORWARD = 1;
  /**
   * The backward command.
   */
  public static final int BACKWARD = 0;
  /**
   * The left motor ID.
   */
  public static final int LEFT = 1;
  /**
   * The right motor ID.
   */
  public static final int RIGHT = 0;
  /**
   * The main object which handles the methods to get access to the resources
   * connected to the board.
   */
  private static Board board;
  /**
   * The current command.
   */
  private int command = Commands.UNUSED;
  /**
   * The debug object.
   */
  private Debug debug;

  public Motor(int id) throws IOException, InterruptedException {
    command = id == LEFT ? LEFT_COMMAND : RIGHT_COMMAND;
    board = Board.getInstance();
  }

  /**
   * Moves the motor in the direction at the given speed.
   * @param direction The direction of the movement.
   * @param speed
   * @return A status code.
   * @throws IOException
   */
  public int move(int direction, int speed) throws IOException {
    return board.writeI2c(command, direction, speed, Commands.UNUSED);
  }
}