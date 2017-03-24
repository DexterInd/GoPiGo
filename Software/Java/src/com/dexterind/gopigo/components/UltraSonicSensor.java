/*
 * #%L
 * **********************************************************************
 * ORGANIZATION  :  DexterIndustries
 * PROJECT       :  GoPiGo Java Library
 * FILENAME      :  UltraSonicSensor.java
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
 * It get access to the ultrasonic sensor distance calculation.
 * It also allows to enable or disable it.
 * @author marcello
 *
 */
public class UltraSonicSensor {
  /**
   * The main object which handles the methods to get access to the resources
   * connected to the board.
   */
  private static Board board;
  /**
   * The instance of the current object.
   */
  private static UltraSonicSensor instance = null;
  /**
   * The current pin. It can be configured through the setPin() method.
   */
  private int pin = 0;
  /**
   * The debug object.
   */
  private Debug debug;

  public UltraSonicSensor() throws IOException, InterruptedException {
    board = Board.getInstance();
  }

  /**
   * Provides a global point of access to the UltraSonicSensor instance.
   * @return  the <code>UltraSonicSensor</code> instance.
   */
  public static UltraSonicSensor getInstance() throws IOException, InterruptedException {
    if(instance == null) {
      instance = new UltraSonicSensor();
    }
    return instance;
  }

  /**
   * Sets the pin to use for the sensor.
   * @param pin The number of the pin where the sensor is attached.
   */
  public void setPin(int pin) {
    this.pin = pin;
  }

  /**
   * Reads the distance through the ultrasonic sound.
   * @return The distance in centimeters.
   * @throws IOException
   */
  public int getDistance() throws IOException {
    board.writeI2c(Commands.US, pin, Commands.UNUSED, Commands.UNUSED);

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
}