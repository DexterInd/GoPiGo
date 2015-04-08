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
 * A status event is fired at every change to the GoPiGo status.
 * @author marcello
 *
 */
public class StatusEvent extends EventObject {

  private static final long serialVersionUID = -2236533038040111378L;
  /**
   * The status of the event. All the status are referenced into the
   *  Statuses static class.
   */
  public int status;

  public StatusEvent(Object source) {
    super(source);
  }

  public StatusEvent(Object source, int status) {
      this(source);
      this.status = status;
   }
}