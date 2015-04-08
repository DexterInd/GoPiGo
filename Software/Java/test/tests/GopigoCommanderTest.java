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
package tests;

import com.dexterind.gopigo.*;
import com.dexterind.gopigo.components.Motor;
import com.dexterind.gopigo.components.UltraSonicSensor;
import com.dexterind.gopigo.events.*;
import com.dexterind.gopigo.utils.Statuses;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class GopigoCommanderTest implements GopigoListener {
  private static int ultrasonicPin = 15;

  private static Gopigo gopigo = null;

  public GopigoCommanderTest() throws IOException, InterruptedException {
    System.out.println("-----------------------------------------------------");
    System.out.println("Welcome to the GoPiGo test application");
    System.out.println("When asked, insert a command to test your GoPiGo");
    System.out.println("(!) For a complete list of commands, please type help");
    System.out.println(" ----------------------------------------------------");

    gopigo = Gopigo.getInstance();
    gopigo.addListener(this);

    gopigo.ultraSonicSensor.setPin(ultrasonicPin);
    gopigo.setMinVoltage(5.5);
    gopigo.init();
  }

  // Event handlers
  public void onStatusEvent(StatusEvent event) {
    System.out.println("\f");
    System.out.println("[Status Changed]");
    switch (event.status) {
      case Statuses.INIT:
        System.out.println("OK Init");
        break;
      case Statuses.HALT:
        System.out.println("WARN Halt");
        break;
    }
    try {
      askForCommand();
    } catch (InterruptedException e) {
      e.printStackTrace();
    }
  }

  public void onVoltageEvent(VoltageEvent event) {
    System.out.println("\f");
    System.out.println("[Voltage Event]");
    System.out.println(event.value + " Volts");
    try {
      askForCommand();
    } catch (InterruptedException e) {
      e.printStackTrace();
    }
  }

  private static void askForCommand() throws InterruptedException {
    System.out.print("What would you like me to do? > ");

    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

    String command = null;
    String outputMessage = null;
    String outputValue = null;

    try {
      command = br.readLine();

      if (command.equals("help")) {
        System.out.println("");
        System.out.println("reset => performs a reset of LEDs and servo motor (also sets the speed to 255)");
        System.out.println("voltage limits => returns the minimum and the critical voltage values)");
        System.out.println("left motor test => test the left motor at its maximum speed (it will also turn ON the left LED)");
        System.out.println("right motor test => test the right motor at its maximum speed (it will also turn ON the right LED)");
        System.out.println("left led on => turn left led on");
        System.out.println("left led off => turn left led off");
        System.out.println("right led on => turn right led on");
        System.out.println("right led off => turn right led off");
        System.out.println("move forward => moves the GoPiGo forward");
        System.out.println("move backward => moves the GoPiGo backward");
        System.out.println("turn left => turns the GoPiGo to the left");
        System.out.println("turn right => turns the GoPiGo to the right");
        System.out.println("stop => stops the GoPiGo");
        System.out.println("increase speed => increases the motors speed");
        System.out.println("decrease speed => decreases the motors speed");
        System.out.println("voltage => returns the voltage value");
        System.out.println("servo test => performs a servo test");
        System.out.println("ultrasonic distance => returns the distance from an object");
        System.out.println("move forward with pid => moves the GoPiGo forward with PID");
        System.out.println("move backward with pid => moves the GoPiGo backward with PID");
        System.out.println("rotate left => rotates the GoPiGo to the left");
        System.out.println("rotate right => rotates the GoPiGo to the right");
        System.out.println("set encoder targeting => sets the encoder targeting");
        System.out.println("firmware version => returns the firmware version");
        System.out.println("exit => exits from this test");
        System.out.println("");
      }
      if (command.equals("reset")) {
        outputMessage = "Reset";
        outputValue = "1";
        gopigo.reset();
      }
      if (command.equals("voltage limits")) {
        outputMessage = "Voltage limits";
        outputValue = "Min. voltage: " + gopigo.getMinVoltage() + ", Ciritcal voltage: " + gopigo.getCriticalVoltage();
      }
      if (command.equals("left motor test")) {
        outputMessage = "Left motor moving - FORWARD (" + Motor.FORWARD + ")";
        outputValue = Integer.toString(gopigo.motorLeft.move(Motor.FORWARD, 255));
        gopigo.ledRight.off();
        gopigo.ledLeft.on();
      }
      if (command.equals("right motor test")) {
        outputMessage = "Right motor moving - BACKWARD (" + Motor.BACKWARD + ")";
        outputValue = Integer.toString(gopigo.motorRight.move(Motor.BACKWARD, 255));
        gopigo.ledRight.on();
        gopigo.ledLeft.off();
      }
      if (command.equals("left led on")) {
        outputMessage = "Left led ON";
        outputValue = Integer.toString(gopigo.ledLeft.on());
      }
      if (command.equals("left led off")) {
        outputMessage = "Left led OFF";
        outputValue = Integer.toString(gopigo.ledLeft.off());
      }
      if (command.equals("right led on")) {
        outputMessage = "Right led ON";
        outputValue = Integer.toString(gopigo.ledRight.on());
      }
      if (command.equals("right led off")) {
        outputMessage = "Right led OFF";
        outputValue =  Integer.toString(gopigo.ledRight.off());
      }
      if (command.equals("move forward") || command.equals("w")) {
        outputMessage = "Move forward";
        outputValue =  Integer.toString(gopigo.motion.forward(false));
      }
      if (command.equals("turn left") || command.equals("a")) {
        outputMessage = "Turn left";
        outputValue =  Integer.toString(gopigo.motion.left());
      }
      if (command.equals("turn right") || command.equals("d")) {
        outputMessage = "Turn right";
        outputValue =  Integer.toString(gopigo.motion.right());
      }
      if (command.equals("move backward") || command.equals("s")) {
        outputMessage = "Move backward";
        outputValue =  Integer.toString(gopigo.motion.backward(false));
      }
      if (command.equals("stop") || command.equals("x")) {
        outputMessage = "Stop";
        outputValue =  Integer.toString(gopigo.motion.stop());
        gopigo.ledRight.off();
        gopigo.ledLeft.off();
      }
      if (command.equals("increase speed") || command.equals("t")) {
        outputMessage = "Increase speed";
        outputValue =  Integer.toString(gopigo.motion.increaseSpeed());
      }
      if (command.equals("decrease speed") || command.equals("g")) {
        outputMessage = "Decrease speed";
        outputValue =  Integer.toString(gopigo.motion.decreaseSpeed());
      }
      if (command.equals("voltage")) {
        outputMessage = "Voltage";
        outputValue =  Double.toString(gopigo.board.volt());
      }
      if (command.equals("servo test") || command.equals("b")) {
        outputMessage = "Servo test";
        outputValue =  Integer.toString(gopigo.servo.move(90));
      }
      if (command.equals("exit") || command.equals("z")) {
        System.out.println("Ok, bye!");
        System.exit(1);
      }
      if (command.equals("ultrasonic distance") || command.equals("u")) {
        outputMessage = "Ultrasonic Distance (cm)";
        outputValue =  Integer.toString(UltraSonicSensor.getInstance().getDistance());
      }
      if (command.equals("l")) {
        // TODO
      }
      if (command.equals("move forward with pid") || command.equals("i")) {
        outputMessage = "Move forward with PID";
        outputValue =  Integer.toString(gopigo.motion.forward(true));
      }
      if (command.equals("move backward with pid") || command.equals("k")) {
        outputMessage = "Move backward with PID";
        outputValue =  Integer.toString(gopigo.motion.backward(true));
      }
      if (command.equals("rotate left") || command.equals("n")) {
        outputMessage = "Rotate left";
        outputValue =  Integer.toString(gopigo.motion.leftWithRotation());
      }
      if (command.equals("rotate right") || command.equals("m")) {
        outputMessage = "Rotate right";
        outputValue =  Integer.toString(gopigo.motion.rightWithRotation());
      }
      if (command.equals("set encoder targeting") || command.equals("y")) {
        outputMessage = "Set encoder targeting (1,1,18)";
        outputValue =  Integer.toString(gopigo.encoders.targeting(1, 1, 18));
      }
      if (command.equals("firmware version") || command.equals("f")) {
        outputMessage = "Firmware version";
        outputValue =  Float.toString(gopigo.board.version());
      }

      if (outputMessage != null && outputValue != null) {
        System.out.println(outputMessage + "::" + outputValue);
      }

      askForCommand();
    } catch (IOException e) {
      System.out.println("IO error trying to read your command!");
      System.exit(1);
    }
  }
}
