import ir_receiver
import time 

while True:
    inp= ir_receiver.nextcode()
    if len(inp)!=0:
        print inp
    time.sleep(.01) #Wait a bit before reading again