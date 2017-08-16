# Test IR Receiver
# This program tests the IR reciever function built into the GoPiGo2.
# To test, connect the IR receiver to port D11 on the GoPiGo2.
# Run the program.  

from gopigo import *
import sys

while True:

    time.sleep(0.01)
    print(ir_read())
