##IR remote control

### Thisfolder contains the files to control the GoPiGo with and IR remote similar to the one used with TV and AC's 

**_Files:_**
- **gopigo_ir_control_test.py** : Used to test and record the button presse on the remote
- **gopigo_ir_control_bot.py** : Program to control the GoPiGo using the IR Remote 
- **setup.py** : Installation file for the GoPiGo (use only if you are not using Dexter Industries SD Card)

**Usage:_**
First run the **gopigo_ir_control_test.py** and find out the IR codes for the button press on the remote.

Once you have found the unique code in each of the button press, program them in the **gopigo_ir_control_bot.py** to control the GoPiGo when you press the buttons on the remote