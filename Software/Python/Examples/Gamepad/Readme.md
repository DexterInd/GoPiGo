## USB Gamepad Example
### This example controls the GoPiGo using a Logitech F710 Gamepad.

![Logitech Gamepad and the Raspberry Pi Robot](https://raw.githubusercontent.com/egoebelbecker/GoPiGo/master/Software/Python/Examples/Gamepad/gpg_and_f710.jpg "GoPiGo Raspberry Pi Robot controlled with a Logitech Gamepad")


**Files:**
- gamepad.py : Example of using a usb gamepad to control the GoPiGo
- show_buttons.py : Python script that prints button values as they are pressed on the gamepad


**Overview:**

For an in-depth explanation of these script see [this blog post] (http://egoebelbecker.me/2015/06/10/raspberry-pi-and-gamepad-programming-part-2-controlling-the-gopigo/)

The example script uses buttons on the gamepad to control the GoPiGo's movement. The script is written for a Logitech F710, but other gamepads should work. Use the showbuttons script to display the button values on your gamepad and modify the script.

**Usage**
- Connect the controller.
- Open a terminal session via vnc or ssh.
- Make sure gamepad.py is executable:   chmod +x gamepad.py
- Run gamepad.py.
- The script will print the direction you specify via the gamepad, as well as move the GoPiGo.
- For the Logitech gamepad A-B-X-Y control direction.
- Clicking on the right hand joystick stops the GoPiGo.
- LB and RB on the front of the Gamepad control speed.
- See the script comments for how to modify for different controllers.

