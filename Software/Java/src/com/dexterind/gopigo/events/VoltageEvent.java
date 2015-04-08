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
package com.dexterind.gopigo.events;

import java.util.EventObject;

/**
 * A voltage event is fired by the voltage check task and it contains the current
 * voltage value in volts.
 * @author marcello
 *
 */
public class VoltageEvent extends EventObject {

  private static final long serialVersionUID = 5992043874332938157L;
  /**
   * The value of the voltage.
   */
  public double value;

  public VoltageEvent(Object source) {
    super(source);
  }

  public VoltageEvent(Object source, double value) {
      this(source);
      this.value = value;
   }
}