#Controls.py
#control the robot according to data from client
#By Tyler Spadgenske

import time, socket, select
from gopigo import *

class Control():
    def __init__(self):
        #Setup servo
        self.pos = 110
        enable_servo()
        servo(self.pos)

        self.first = True

        #Setup server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = ''
        self.port = 5150
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print 'Listing for a client...'
        self.client, self.addr = self.server.accept()
        print 'Accepted connection from ', self.addr
        self.msg = 'stop'

    def wait_for_cmd(self):
        while True:
            self.old_cmd = self.msg
            self.client, self.addr = self.server.accept()
        
            data = self.client.recv(1024)   
            self.msg = bytes.decode(data)

            self.parse(self.msg)
            self.client.close()
            
    def parse(self, cmd):
        if cmd == 'forward':
            fwd()
            time.sleep(.05)
        if cmd == 'backward':
            bwd()
            time.sleep(.05)
        if cmd == 'left':
            left()
            time.sleep(.05)
        if cmd == 'right':
            right()
            time.sleep(.05)
        if cmd == 'servo right':
            self.pos -= 5
            if self.pos < 0:
                self.pos = 0
        if cmd == 'servo left':
            self.pos += 5
            if self.pos > 180:
                self.pos = 180
        if cmd == 'take picture':
            self.take_picture()
        if cmd == 'stop':
            stop()
        if cmd == '11':
            led_on(LED_L)
            led_on(LED_R)
        if cmd == '10':
            led_on(LED_L)
            led_off(LED_R)
        if cmd == '01':
            led_off(LED_L)
            led_on(LED_R)
        if cmd == '00':
            led_off(LED_L)
            led_off(LED_R)
        servo(self.pos)
        
    def take_picture(self):
        try:
            pic = open('pic.txt', 'r')
            pic.close()
            self.first = False
        except:
            if self.first:
                pic = open('pic.txt', 'w+')
                pic.write('True')
                pic.close()
            self.first = True

if __name__ == '__main__':
    system = Control()
    system.wait_for_cmd()
