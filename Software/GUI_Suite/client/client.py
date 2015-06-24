#GoPiGo GUI Client v1.0
#copyright (c) 2015 Tyler Spadgenske GPL v2

import socket, select
from subprocess import Popen
import pygame
import sys, os, time 
from Tkinter import *

pygame.init()

'''Classes and functions for IP retrieval'''
class takeInput(object):

    def __init__(self,requestMessage):
        self.root = Tk()
        self.string = ''
        self.frame = Frame(self.root)
        self.frame.pack()        
        self.acceptInput(requestMessage)

    def acceptInput(self,requestMessage):
        r = self.frame

        k = Label(r,text=requestMessage)
        k.pack(side='left')
        self.e = Entry(r,text='Submit')
        self.e.pack(side='left')
        self.e.focus_set()
        b = Button(r,text='Submit',command=self.gettext)
        b.pack(side='right')

    def gettext(self):
        self.string = self.e.get()
        self.root.destroy()

    def getString(self):
        return self.string

    def waitForInput(self):
        self.root.mainloop()

def getText(requestMessage):
    msgBox = takeInput(requestMessage)
    #loop until the user makes a decision and the window is destroyed
    msgBox.waitForInput()
    return msgBox.getString()

class Suite():
    def __init__(self):
        #Get robots ip
        try:
            ip_file = open('ip.txt', 'r')
            self.host = ip_file.readline()
            ip_file.close()
        except:
            self.host = getText('Enter GoPiGo IP address:')
            ip_file = open('ip.txt', 'w+')
            ip_file.write(self.host)

        #Important
        self.PORT=5000

        #Setup window
        os.environ ['SDL_VIDEO_WINDOW_POS'] = 'center'
        self.screen = pygame.display.set_mode((800,500),0)
        pygame.display.set_caption('GoPiGo GUI Client v1.0 Beta')

        #Setup colors
        self.WHITE = (255,255,255)
        self.BLUE = (0,0,255)
        self.GRAY = (153, 153, 153)
        
        #Setup fonts
        self.text_font = pygame.font.SysFont(None, 30)

        #Random variables
        self.update = True
        self.progress = 'Searching for robot...'
        self.load_error = False
        self.exit = False
        self.left_led = False
        self.right_led = False
        self.old_leds = [self.left_led, self.right_led]

        self.dir = 'stop'
        self.old_dir = self.dir
        self.servo_dir = 'stop'
        self.snap_pic = False

        #Loading clock
        self.start_time = time.time()
        self.total_time = 0
        #Receive clock
        self.receive_clock = time.time()

        #Robot logo stuff
        self.robot_logo = pygame.image.load('images/robot-logo.png')
        self.robot_logo_rect = self.robot_logo.get_rect()
        self.robot_logo_rect.centerx = self.screen.get_rect().centerx
        self.robot_logo_rect.centery = self.screen.get_rect().centery - 100

        #Controls
        self.off = pygame.image.load('images/leds_off.png')
        self.left_on = pygame.image.load('images/left_on.png')
        self.right_on = pygame.image.load('images/right_on.png')
        self.on = pygame.image.load('images/leds_on.png')
        self.controls_rect = self.off.get_rect()
        self.controls_rect.centerx = self.screen.get_rect().centerx
        self.controls_rect.centery = self.screen.get_rect().centery + 170

        #Progress message stuff
        self.progress_text = self.text_font.render(self.progress, True, self.GRAY, self.WHITE)
        self.progress_rect = self.progress_text.get_rect()
        self.progress_rect.centerx = self.screen.get_rect().centerx
        self.progress_rect.centery = self.screen.get_rect().centery + 60

    def setup(self):
        '''GUI interface during startup proceedure'''
        while True:
            if self.update:
                self.progress_text = self.text_font.render(self.progress, True, self.GRAY, self.WHITE)
                self.screen.fill(self.WHITE)
                self.screen.blit(self.robot_logo, self.robot_logo_rect)

            self.screen.blit(self.progress_text, self.progress_rect)
            if not self.load_error:
                self.load()
            pygame.display.update()
            self.events()
            if self.exit:
                self.controls_connect()
                if not self.load_error:
                    break
            
    def load(self):
        '''Draws the circle loading animation'''
        #Draw loading circles at position relative to time
        if time.time() - self.start_time > .5:
            pygame.draw.circle(self.screen, self.BLUE, (360, 265), 5, 0)
        if time.time() - self.start_time > 1:
            pygame.draw.circle(self.screen, self.BLUE, (380, 265), 5, 0)
        if time.time() - self.start_time > 1.5:
            pygame.draw.circle(self.screen, self.BLUE, (400, 265), 5, 0)
        if time.time() - self.start_time > 2:
            pygame.draw.circle(self.screen, self.BLUE, (420, 265), 5, 0)
        if time.time() - self.start_time > 2.5:
            pygame.draw.circle(self.screen, self.BLUE, (440, 265), 5, 0)
        if time.time() - self.start_time > 3:
            self.start_time = time.time()
            self.total_time += 1

        if self.total_time == 2:
            self.progress = 'Connecting to robot...'
        if self.total_time == 3:
            self.progress = 'Detecting camera...'
        if self.total_time == 4:
            self.exit = True

    def connect(self):
        '''Connects to camera stream'''
        self.clientsocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect((self.host, self.PORT))

    def controls_connect(self):
        '''Connects to robot control server'''
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.control_port = 5150
        
        try:
            self.server.connect((self.host, self.control_port))
            self.data = self.server.recv(1024)
            msg = bytes.decode(self.data)
        except:
            self.load_error = True
            self.progress = 'Cannot connect to robot'
            try:
                os.remove('ip.txt')
            except:
                pass

    def send_data(self, data):
        '''send control data to server'''
        self.server.send(str.encode(str(data)))
            
    def main(self):
        '''Main program execution'''
        while True:
            self.screen.fill(self.WHITE)
            #Blit correct control pannel according to LED state
            if self.left_led == False and self.right_led == False:
                self.screen.blit(self.off, self.controls_rect)
            elif self.right_led:
                self.screen.blit(self.right_on, self.controls_rect)
            elif self.left_led:
                self.screen.blit(self.left_on, self.controls_rect)
            if self.left_led and self.right_led:
                self.screen.blit(self.on, self.controls_rect)
            received = []

            self.connect()
            # loop .recv, it returns empty string when done, then transmitted data is completely received
            while True:
                recvd_data = self.clientsocket.recv(230400)
                if not recvd_data:
                    break
                else:
                    received.append(recvd_data)

            dataset = ''.join(received)
            image = pygame.image.fromstring(dataset,(480,320),"RGB") # convert received image from string
            self.screen.blit(image,(160,20)) # "show image" on the screen
            pygame.display.update()
            self.events()

            #Send command if new
            self.send_data(self.dir)
            if self.old_leds[0] != self.left_led or self.old_leds[1] != self.right_led:
                self.old_leds = [self.left_led, self.right_led]
                if self.left_led and self.right_led:
                    s = '11'
                elif self.left_led:
                    s = '10'
                elif self.right_led:
                    s = '01'
                else:
                    s = '00'
                    
                self.send_data(s)

    def events(self):
        '''handles keyboard and mouse events'''
        # check for quit events
        for event in pygame.event.get():
            #Keyboard events
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Check for LED events
                self.old_leds = [self.left_led, self.right_led]
                if event.pos[0] < 97 and event.pos[1] > 381:
                    if self.left_led:
                        self.left_led = False
                    else:
                        self.left_led = True
                if event.pos[0] > 697 and event.pos[1] > 381:
                    if self.right_led:
                        self.right_led = False
                    else:
                        self.right_led = True

                self.old_dir = self.dir
                #Check for the remaining control events
                if event.pos[1] > 420:
                    if event.pos[0] > 127 and event.pos[0] < 200:
                        self.dir = 'servo left'
                    if event.pos[0] > 200 and event.pos[0] < 276:
                        self.dir = 'servo right'
                    if event.pos[0] > 322 and event.pos[0] < 420:
                        self.dir = 'take picture'
                    if event.pos[0] > 449 and event.pos[0] < 525:
                        self.dir = 'left'
                    if event.pos[0] > 525 and event.pos[0] < 600:
                        self.dir = 'backward'
                    if event.pos[0] > 600 and event.pos[0] < 676:
                        self.dir = 'right'
                if event.pos[1] > 345 and event.pos[1] < 420 and event.pos[0] > 525 and event.pos[0] < 600:
                    self.dir = 'forward'

            if event.type == pygame.MOUSEBUTTONUP:
                self.dir = 'stop'
                
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    client = Suite()
    client.setup()
    client.main()
