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
package com.dexterind.gopigo.utils;

public class Statuses {
  /**
   * The OK status. This is returned by all the I2C methods.
   */
  public static final int OK = 1;
  /**
   * The ERROR status. This is returned by the I2C methods in case of issues.
   */
  public static final int ERROR = -1;
  /**
   * The INIT status.
   */
  public static final int INIT = 2;
  /**
   * The HALT status.
   */
  public static final int HALT = 3;

  public Statuses(){}
}