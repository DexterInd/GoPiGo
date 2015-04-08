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
import java.io.PrintWriter;
import java.io.StringWriter;
import java.nio.ByteBuffer;
import java.util.*;

import com.dexterind.gopigo.*;
import com.dexterind.gopigo.events.StatusEvent;
import com.dexterind.gopigo.utils.*;

import com.pi4j.io.i2c.I2CBus;
import com.pi4j.io.i2c.I2CDevice;
import com.pi4j.io.i2c.I2CFactory;
import com.pi4j.system.NetworkInfo;
import com.pi4j.system.SystemInfo;

/**
 * Defines all the methods to get access to the resources connected to the board.
 * It also returns the status, the voltage and the firmware version of the board.
 * @author marcello
 *
 */
public class Board {
  /**
   * The instance of the current object.
   */
  private static Board instance = null;
  /**
   * The I2CDevice object.
   */
  private final I2CDevice device;
  /**
   * The output mode for the pin.
   */
  private static final byte PIN_MODE_OUTPUT = 1;
  /**
   * The input mode for the pin.
   */
  private static final byte PIN_MODE_INPUT = 0;
  /**
   * The device's address.
   */
  private static final byte ADDRESS = 0x08;
  /**
   * The debug object.
   */
  private Debug debug;

  public Board() throws IOException, InterruptedException {
    int busId;

    String type = SystemInfo.getBoardType().name();

    if (type.indexOf("ModelA") > 0) {
      busId = I2CBus.BUS_0;
    } else {
      busId = I2CBus.BUS_1;
    }

    final I2CBus bus = I2CFactory.getInstance(busId);
    device = bus.getDevice(ADDRESS);
  }

  /**
   * Provides a global point of access to the Board instance.
   * @return  the <code>Board</code> instance.
   */
  public static Board getInstance() throws IOException, InterruptedException {
    if(instance == null) {
      instance = new Board();
    }
    return instance;
  }

  /**
   * Writes the bytes to the I2C device.
   * @param bytes The buffer to write.
   * @return A status code.
   * @throws IOException
   */
  public int writeI2c(int... bytes) throws IOException {
    if (Gopigo.getInstance().isHalt()) {
      Gopigo.getInstance().onHalt();
    }
    // Convert array: int[] to byte[]
    final ByteBuffer byteBuffer = ByteBuffer.allocate(bytes.length);
    for (int i = 0, len = bytes.length; i < len; i++) {
      byteBuffer.put((byte) bytes[i]);
    }
    sleep(100); // TODO: Is correct to have this here or we let the external calls to handle the sleep?
    device.write(0xfe, byteBuffer.array(), 0, byteBuffer.limit());
    return Statuses.OK;
  }

  /**
   * Reads the number of bytes from the I2C device.
   * @param numberOfBytes The length of the buffer to read.
   * @return The buffer.
   * @throws IOException
   */
  public byte[] readI2c(int numberOfBytes) throws IOException {
    if (Gopigo.getInstance().isHalt()) {
      Gopigo.getInstance().onHalt();
    }
    byte[] buffer = new byte[numberOfBytes];
    device.read(1, buffer, 0, buffer.length);
    return buffer;
  }

  /**
   * Executes a digital read on the pin.
   * @param pin The pin to use for the reading.
   * @return The read bytes.
   * @throws IOException
   */
  public int digitalRead(int pin) throws IOException {
    if (Gopigo.getInstance().isHalt()) {
      Gopigo.getInstance().onHalt();
    }
    writeI2c(Commands.DIGITAL_READ, pin, Commands.UNUSED, Commands.UNUSED);
    return device.read() & 0xff;
  }

  /**
   * Executes a digital write on the pin.
   * @param pin The ping to use for the writing.
   * @param value The value to write.
   * @return A status code.
   * @throws IOException
   */
  public int digitalWrite(int pin, int value) throws IOException {
    if (Gopigo.getInstance().isHalt()) {
      Gopigo.getInstance().onHalt();
    }
    return writeI2c(Commands.DIGITAL_WRITE, pin, value, Commands.UNUSED);
  }

  /**
   * Executes an analog read on the pin.
   * @param pin The ping to use for the reading.
   * @return The read value.
   * @throws IOException
   */
  public int analogRead(int pin) throws IOException {
    if (Gopigo.getInstance().isHalt()) {
      Gopigo.getInstance().onHalt();
    }
    if (pin == 1) {
      writeI2c(Commands.ANALOG_READ, pin, Commands.UNUSED, Commands.UNUSED);
      sleep(100);
      byte[] b1 = readI2c(1);
      byte[] b2 = readI2c(2);
      int val1 = (int)b1[0] & 0xFF;
      int val2 = (int)b2[0] & 0xFF;

      return val1 * 256 + val2;
    } else {
      return -2;
    }
  }

  /**
   * Executes an analog write on the pin.
   * @param pin The ping to use for the writing.
   * @param value The value to write.
   * @return A status code.
   * @throws IOException
   */
  public int analogWrite(int pin, int value) throws IOException {
    if (Gopigo.getInstance().isHalt()) {
      Gopigo.getInstance().onHalt();
    }
    if (pin == 10) {
      writeI2c(Commands.ANALOG_WRITE, pin, value, Commands.UNUSED);
      sleep(5);
      return Statuses.OK;
    } else {
      return -2; // TODO: Which kind of status is "-2"?
    }
  }

  /**
   * Sets the pin mode to use on the pin.
   * @param pin The ping to set.
   * @param pinMode The mode to set. 1 is OUTPUT, 0 is INPUT
   * @return A status code.
   * @throws IOException
   */
  public int setPinMode(int pin, int pinMode) throws IOException {
    if (Gopigo.getInstance().isHalt()) {
      Gopigo.getInstance().onHalt();
    }
    return writeI2c(Commands.PIN_MODE, pin, pinMode, Commands.UNUSED);
  }

  /**
   * Executes a sleep on the thread for the number of milliseconds.
   * @param msec The value of the sleep in milliseconds.
   */
  public void sleep(int msec) {
    try {
      Thread.sleep(msec);
    } catch (InterruptedException e) {
      throw new IllegalStateException(e);
    }
  }

  /**
   * Initializes the board executing a writing test catching the error.
   */
  public void init() {
    try {
      device.write(0xfe, (byte)0x04);
    } catch (IOException e) {
      StringWriter sw = new StringWriter();
      e.printStackTrace(new PrintWriter(sw));
      String exceptionDetails = sw.toString();
      debug.log(Debug.SEVERE, exceptionDetails);
      Gopigo.getInstance().halt();
    }
  }

  /**
   * Returns the current voltage on the board.
   * @return The current voltage in volts.
   * @throws IOException
   */
  public double volt() throws IOException {
    writeI2c(Commands.VOLT, Commands.UNUSED, Commands.UNUSED, Commands.UNUSED);
    sleep(100);

    byte[] b1 = readI2c(1);
    byte[] b2 = readI2c(1);
    int val1 = (int)b1[0] & 0xFF;
    int val2 = (int)b2[0] & 0xFF;

    if (val1 != -1 && val2 != -1) {
      double v = val1 * 256 + val2;
      v = (5 * (float) v / 1024) / .4;
      v = Math.round(v * 100.0) / 100.0;
      return v;
    } else {
      return Statuses.ERROR;
    }
  }

  /**
   * Returns the firmware version.
   * @return The firmware version.
   * @throws IOException
   */
  public float version() throws IOException {
    writeI2c(Commands.FW_VER, Commands.UNUSED, Commands.UNUSED, Commands.UNUSED);
    sleep(100);

    byte[] ver = readI2c(1);
    readI2c(1);

    return (float)ver[0] / 10;
  }

  /**
   * Reads the current status.
   * @return Returns the current status.
   * @throws IOException
   */
  public int[] readStatus() throws IOException {
    byte[] status = readI2c(1);
    int[] status_reg = new int[2];

    status_reg[0] = status[0] & (1 << 0);
    status_reg[1] = (status[0] & (1 << 1)) / 2;

    return status_reg;
  }
}