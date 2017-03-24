/*
 * #%L
 * **********************************************************************
 * ORGANIZATION  :  DexterIndustries
 * PROJECT       :  GoPiGo Java Library
 * FILENAME      :  Debug.java
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
package com.dexterind.gopigo.utils;

import java.io.IOException;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.util.Properties;
import java.util.logging.FileHandler;
import java.util.logging.Logger;
import java.util.logging.SimpleFormatter;

/**
 * If the debug mode is ON this class will write the given log into a log file.
 * It's possible to define the log dir. and the log filename from the configuration file.
 * @author marcello
 *
 */
public class Debug {
  /**
   * The logger object.
   */
  private Logger logger;
  /**
   * The log file handler.
   */
  private FileHandler fh;

  /**
   * The "finest" log level.
   */
  public static final int FINEST = 1;
  /**
   * The "finer" log level.
   */
  public static final int FINER = 2;
  /**
   * The "fine" log level.
   */
  public static final int FINE = 3;
  /**
   * The "config" log level.
   */
  public static final int CONFIG = 4;
  /**
   * The "info" log level.
   */
  public static final int INFO = 5;
  /**
   * The "warning" log level.
   */
  public static final int WARNING = 6;
  /**
   * The "severe" log level.
   */
  public static final int SEVERE = 7;

  /**
   * The flag to set to enable or disable the debug.
   */
  private Boolean debug = false;
  /**
   * The default directory where the log will be created.
   */
  private String logDir = "/var/log/gopigo";
  /**
   * The default filename for the log.
   */
  private String logFile = "all.log";

  public Debug(String target) {
    Properties prop = new Properties();
    InputStream input = null;

    try {
      String configProp = System.getProperty("config") == null ? "default" : System.getProperty("config");
      input = new FileInputStream(System.getProperty("user.dir") + "/../config/" + configProp + ".properties");
      prop.load(input);

      debug = Boolean.valueOf(prop.getProperty("debug"));
      logDir = prop.getProperty("logDir");
      logFile = prop.getProperty("logFile");
    } catch (IOException e) {
      e.printStackTrace();
    } finally {
      if (input != null) {
        try {
          input.close();
        } catch (IOException e) {
          e.printStackTrace();
        }
      }
    }

    logger = Logger.getLogger(target);
    try {
      File file = new File(logDir);
      if (!file.exists()) {
        if (file.mkdir()) {
          System.out.println("Log Directory is created!");
        } else {
          System.out.println("Failed to create log directory!");
        }
      }
      fh = new FileHandler(logDir + "/" + logFile, true);
      logger.addHandler(fh);
      logger.setUseParentHandlers(false);
      // this one disables the console log
      SimpleFormatter formatter = new SimpleFormatter();
      fh.setFormatter(formatter);
    } catch (SecurityException e) {
      e.printStackTrace();
    } catch (IOException e) {
      e.printStackTrace();
    }
  }

  /**
   * Writes the log message with the given level. If the debug is disabled then returns immediately.
   * @param level The level of the log to use.
   * @param message The message of the log to write.
   */
  public void log(int level, String message) {
    if (!debug) {
      return;
    }

    switch (level) {
      default:
      case Debug.FINEST:
        logger.finest(message);
        break;
      case Debug.FINER:
        logger.finer(message);
        break;
      case Debug.FINE:
        logger.fine(message);
        break;
      case Debug.CONFIG:
        logger.config(message);
        break;
      case Debug.INFO:
        logger.info(message);
        break;
      case Debug.WARNING:
        logger.warning(message);
        break;
      case Debug.SEVERE:
        logger.severe(message);
        break;
    }
  }
}
