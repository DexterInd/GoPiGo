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
package com.dexterind.gopigo;

import java.io.IOException;
import java.util.*;
import java.util.concurrent.CopyOnWriteArrayList;

import com.dexterind.gopigo.behaviours.*;
import com.dexterind.gopigo.components.*;
import com.dexterind.gopigo.events.*;
import com.dexterind.gopigo.utils.*;

/**
 * The main class for the Gopigo. It instanciates all the components and
 * behaviours and is in charge to handle the events.
 * @author marcello
 *
 */
public final class Gopigo {
  /**
   *  The instance of the current object.
   */
  private static Gopigo instance;
  /**
   * The flag for the initialized status.
   */
  private boolean isInit = false;
  /**
   * The flag for the halted status.
   */
  private boolean isHalt = false;
  /**
   * The timer which will be in charge to check the voltage value.
   */
  private Timer voltageTimer;
  /**
   * The time in milliseconds between successive task executions.
   */
  private int voltageTimerTime = 60000;
  /**
   * The minimum voltage value. If the voltage drops under this value a VoltageEvent will be fired.
   */
  private double minVoltage = 5.5;
  /**
   * The critical voltage value. If the voltage drops under this value a VoltageEvent will be fired
   * and the GoPiGo will be flagged as "halted".
   */
  private double criticalVoltage = 1.0;

  /**
   * The main object which handles the methods to get access to the resources
   * connected to the board.
   */
  public Board board;
  /**
   * The encoders.
   */
  public Encoders encoders;
  /**
   * The servo motor.
   */
  public Servo servo;
  /**
   * The ultrasonic sensor.
   */
  public UltraSonicSensor ultraSonicSensor;
  /**
   * The left led.
   */
  public Led ledLeft;
  /**
   * The right led.
   */
  public Led ledRight;
  /**
   * The left motor.
   */
  public Motor motorLeft;
  /**
   * The right motor.
   */
  public Motor motorRight;
  /**
   * The motion behaviour object.
   */
  public Motion motion;
  /**
   * The list of the listeners which are listening for some event.
   */
  private final CopyOnWriteArrayList<GopigoListener> listeners;
  /**
   * The debug object.
   */
  private Debug debug;

  /**
   * Instanciates the components and the behaviours of the Gopigo.
   */
  public Gopigo() {
    debug = new Debug("com.dexterind.gopigo.Gopigo");
    debug.log(Debug.FINEST, "Instancing a new Gopigo!");

    try {
      board = Board.getInstance();
      encoders = Encoders.getInstance();
      servo = Servo.getInstance();
      ultraSonicSensor = UltraSonicSensor.getInstance();
      ledLeft = new Led(Led.LEFT);
      ledRight = new Led(Led.RIGHT);
      motorLeft = new Motor(Motor.LEFT);
      motorRight = new Motor(Motor.RIGHT);
      motion = Motion.getInstance();
    } catch (IOException e) {
      e.printStackTrace();
    } catch (InterruptedException e) {
      e.printStackTrace();
    }

    voltageTimer = new Timer();
    listeners = new CopyOnWriteArrayList<GopigoListener>();
  }

  /**
   * Provides a global point of access to the Gopigo instance.
   * @return  the <code>Gopigo</code> instance.
   */
  public static Gopigo getInstance() {
    if(instance == null) {
      instance = new Gopigo();
    }
    return instance;
  }

  /**
   * Initializes the Gopigo and fires an event once the init is done.
   */
  public void init() {
    debug.log(Debug.FINE, "Init " + isInit);

    board.init();

    if (!isHalt) {
      isInit = true;
      initVoltageCheck();

      StatusEvent statusEvent = new StatusEvent(this, Statuses.INIT);
      fireEvent(statusEvent);
    }
  }

  /**
   * Resets the Gopigo.
   * @throws IOException
   */
  public void reset() throws IOException {
    debug.log(Debug.INFO, "Reset");
    servo.move(motion.directions.get("e"));
    ledLeft.off();
    ledRight.off();
    motion.setSpeed(255);
    free();
  }

  /**
   * Adds a <code>GopigoListener</code> to the listeners list.
   * @param listener The <code>GopigoListener</code> to register.
   */
  public void addListener(GopigoListener listener) {
    debug.log(Debug.INFO, "Adding listener");
    listeners.addIfAbsent(listener);
  }

  /**
   * Removes a <code>GopigoListener</code> from the listeners list.
   * @param listener The <code>GopigoListener</code> to remove.
   */
  public void removeListener(GopigoListener listener) {
    if (listeners != null) {
      debug.log(Debug.INFO, "Removing listener");
      listeners.remove(listener);
    }
  }

  /**
   * Fires an event to the listeners.
   * @param event The event to fire.
   */
  protected void fireEvent(EventObject event) {
    int i = 0;
    debug.log(Debug.INFO, "Firing event [" + listeners.toArray().length + " listeners]");

    for (GopigoListener listener : listeners) {
      debug.log(Debug.INFO, "listener[" + i + "]");
      debug.log(Debug.INFO, event.getClass().toString());

      if (event instanceof StatusEvent) {
        listener.onStatusEvent((StatusEvent) event);
      } else if (event instanceof VoltageEvent) {
        listener.onVoltageEvent((VoltageEvent) event);
      }
      i++;
    }
  }

  /**
   * Initializes a timer which will checks the voltage and will fires and event in case of low voltage.
   */
  private void initVoltageCheck() {
    voltageTimer.scheduleAtFixedRate(new TimerTask() {
      @Override
      public void run() {
        new Thread(new Runnable() {
          public void run() {
            double voltage;
            Boolean dispatchEvent = false;
            try {
              Gopigo.getInstance().debug.log(Debug.INFO, "Voltage check");

              voltage = Gopigo.getInstance().board.volt();
              if (voltage < Gopigo.getInstance().getMinVoltage()) {
                Gopigo.getInstance().debug.log(Debug.WARNING, "Low voltage detected");
                Gopigo.getInstance().free();
                dispatchEvent = true;
              } else if (voltage <= Gopigo.getInstance().getCriticalVoltage()) {
                Gopigo.getInstance().debug.log(Debug.SEVERE, "Critical voltage detected. GoPiGo is now halted.");
                Gopigo.getInstance().halt();
                dispatchEvent = true;
              } else {
                Gopigo.getInstance().free();
              }

              if (dispatchEvent) {
                VoltageEvent voltageEvent = new VoltageEvent(Gopigo.getInstance(), voltage);
                Gopigo.getInstance().fireEvent(voltageEvent);
              }
            } catch (IOException e) {
              e.printStackTrace();
            }
          }
        }).start();
      }
     }, 0, voltageTimerTime);
  }

  /**
   * Sets the GoPiGo free. It removes the "halted" flag if necessary.
   */
  public void free() {
    if (isHalt) {
      debug.log(Debug.INFO, "The GoPigo was halted. I'm setting it free.");
      isHalt = false;
    }
  }
  /**
   * It returns the operativity status.
   * @return True if operative, False if not.
   */
  public Boolean isOperative() {
    return isHalt == false;
  }
  /**
   * Halts the GoPiGo if necessary.
   */
  public void halt() {
    if (!isHalt) {
      debug.log(Debug.WARNING, "The GoPigo was free, now it's halted.");
      isHalt = true;
    }
  }
  /**
   * It returns the halt status.
   * @return True if halted, False if not.
   */
  public Boolean isHalt() {
    return isHalt;
  }
  /**
   * Fires a "HALT" <code>StatusEvent</code>
   */
  public void onHalt() {
    debug.log(Debug.WARNING, "The GoPigo seems to be halted, it will be probably difficult to execute the commands.");
    StatusEvent statusEvent = new StatusEvent(this, Statuses.HALT);
    fireEvent(statusEvent);
  }

  /**
   * Sets the min. voltage value.
   * @param value The minimum voltage value to set.
   */
  public void setMinVoltage(double value) {
    debug.log(Debug.INFO, "Setting minVoltage to " + Double.toString(value));
    minVoltage = value;
  }
  /**
   * Returns the min. voltage value.
   * @return The min. voltage value.
   */
  public Double getMinVoltage() {
    debug.log(Debug.INFO, "Getting minVoltage");
    return minVoltage;
  }
  /**
   * Sets the critical voltage value. Under this value the GoPiGo will be
   * flagged as "halted".
   * @param value The critical voltage value to set.
   */
  public void setCriticalVoltage(double value) {
    debug.log(Debug.INFO, "Setting criticalVoltage to " + Double.toString(value));
    criticalVoltage = value;
  }
  /**
   * Returns the critical voltage value.
   * @return The Critical voltage value.
   */
  public Double getCriticalVoltage() {
    debug.log(Debug.INFO, "Getting criticalVoltage");
    return criticalVoltage;
  }
}