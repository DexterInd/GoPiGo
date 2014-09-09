## Office Cannon
### This example controls the GoPiGo and Office Cannon with a wireless mouse on the USB port.

![A Mobile Office cannon with the Raspberry Pi robot](https://raw.githubusercontent.com/DexterInd/GoPiGo/master/Software/Python/Examples/Office%20Cannon/Office-cannon-with-raspberry-pi.jpg "Office cannon with the Raspberry Pi robot")

**Control:**

- Move the mouse up, down, left or right to control the cannon
- Press any mouse button to start moving the GoPiGo.
- Press Left mouse button to turn the GoPiGo left
- Press Right mouse button to turn the GoPiGo right
- Press both the left and right mouse buttons to stop
- Press the middle mouse button to fire

**Note:**

- The office cannon needs more than the 600mA that is supplied by USB to fire the projectiles.
- For this, the we pull the GPIO 32 to HIGH which allows the USB to supply upto 1.2A.
- The USB power supply is reverted back to normal when the program closes or when the user uses CTRL+CTRL to close the program.
