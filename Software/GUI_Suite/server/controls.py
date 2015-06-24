#Controls.py
#control the robot according to data from client
#By Tyler Spadgenske

import time, socket, select
from gopigo import *
import gopigo

class Control():
    def __init__(self):
        #Setup servo
        self.pos = 110
        enable_servo()
        servo(self.pos)
        disable_servo()

        #Setup server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = ''
        self.port = 5150
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print 'Listing for a client...'
        self.client, self.addr = self.server.accept()
        print 'Accepted connection from ', self.addr
        self.client.send(str.encode('Connected'))
        self.msg = 'stop'

    def wait_for_cmd(self):
        while True:
            self.old_cmd = self.msg
            data = self.client.recv(1024)   
            self.msg = bytes.decode(data)

            self.parse(self.msg)

    def parse(self, cmd):
        if cmd == 'forward':
            fwd()
            time.sleep(.1)
        if cmd == 'backward':
            bwd()
            time.sleep(.1)
        if cmd == 'left':
            left()
            time.sleep(.1)
        if cmd == 'right':
            right()
            time.sleep(.1)
        if cmd == 'servo right':
            self.pos -= 5
            if self.pos < 0:
                self.pos = 0
            enable_servo()
            servo(self.pos)
            time.sleep(1)
            disable_servo()
        if cmd == 'servo left':
            self.pos += 5
            if self.pos > 180:
                self.pos = 180
            enable_servo()
            servo(self.pos)
            time.sleep(1)
            disable_servo()
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

    def take_picture(self):
        print 'take pic'

    def servo_left(self):
        print 'servo l'

    def servo_right(self):
        print 'servo r'

if __name__ == '__main__':
    system = Control()
    system.wait_for_cmd()
