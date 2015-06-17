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
import java.util.Arrays;

import com.dexterind.gopigo.utils.*;

/**
 * It get access to the IR receiver sensor and receive IR signals
 * @author marcello
 *
 */
public class IRReceiverSensor {
  /**
   * The main object which handles the methods to get access to the resources
   * connected to the board.
   */
  private static Board board;
  /**
   * The instance of the current object.
   */
  private static IRReceiverSensor instance = null;
  /**
   * The current pin. It can be configured through the setPin() method.
   */
  private int pin = 0;
  /**
   * The debug object.
   */
  private Debug debug;

  public IRReceiverSensor() throws IOException, InterruptedException {
    board = Board.getInstance();
  }

  /**
   * Provides a global point of access to the UltraSonicSensor instance.
   * @return  the <code>UltraSonicSensor</code> instance.
   */
  public static IRReceiverSensor getInstance() throws IOException, InterruptedException {
    if(instance == null) {
      instance = new IRReceiverSensor();
    }
    return instance;
  }

  /**
   * Sets the pin to use for the sensor.
   * @param pin The number of the pin where the sensor is attached. The given value is increased by one.
   */
  public void setPin(int pin) {
    this.pin = pin + 1;
  }

  /**
   * Reads the IR signal.
   * @return The bytes coming from the sensor.
   * @throws IOException
   */
  public byte[] read() throws IOException {
    write(Commands.UNUSED);
    board.writeI2c(Commands.IR_READ, Commands.UNUSED, Commands.UNUSED, Commands.UNUSED);
    board.sleep(100);
    byte[] b = board.readI2c(22);
    int b1 = (int)b[1] & 0xFF;
    if (b1 != 255) {
        return Arrays.copyOfRange(b, 1, b.length);
    } else {
        return null;
    }
  }
  /**
   * Prepare the IR receiver
   * @return True or False.
   * @throws IOException
   */
  public int write(int value) throws IOException {
    return board.writeI2c(Commands.IR_RECV_PIN, value, Commands.UNUSED, Commands.UNUSED);
  }
}