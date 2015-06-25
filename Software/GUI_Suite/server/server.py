#Stream picamera to clients
#copyright (c) 2015 Tyler Spadgenske

print '++++++++++++++++++++++++++++++'
print 'GoPiGo GUI Server'
print '++++++++++++++++++++++++++++++'

import pygame
import io
import time
import picamera
import yuv2rgb
import socket, sys, os
from subprocess import Popen

if not os.path.exists('images/'):
    os.makedirs('images')
    
print 'Starting control server...'
s = Popen(['python', 'controls.py'])
print 'Server running.'
print 'Setting up camera server...'
port = 5000
pygame.init()
screenSize = (480, 320)
pygame.mouse.set_visible(0)

rgb = bytearray(480 * 320 * 3)
yuv = bytearray(480 * 320 * 3 / 2)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(("",port))
serversocket.listen(1)

camera = picamera.PiCamera()
camera.resolution = (480, 320)
camera.rotation = 180
camera.brightness = 75
camera.contrast = 50

def take_picture():
   try:
      pic = open('pic.txt', 'r')
      pic.close()
      
      try:
         pic_num_file = open('pic_num.txt', 'r')
         pic_num = pic_num_file.readline()
         pic_num_file.close()
         
      except Exception, e:
         print 'Creating uncreated file'
         pic_num_file = open('pic_num.txt', 'w+')
         pic_num_file.write('0')
         pic_num_file.close()
         pic_num_file = open('pic_num.txt', 'r')
         pic_num = pic_num_file.readline()
         pic_num_file.close()

      camera.capture('images/' + pic_num + '.jpg')
      pic_num_file = open('pic_num.txt', 'w')
      pic_num_file.write(str(int(pic_num) + 1))
      pic_num_file.close()
      print 'Took picture ' + pic_num + '.jpg'
      os.remove('pic.txt')
      
   except Exception, f:
      pass

print 'Server Ready'
try:
   while(True):
      take_picture()
      connection, address = serversocket.accept()
      stream = io.BytesIO() # Capture into in-memory stream
      camera.capture(stream, use_video_port=True, format='raw')
      stream.seek(0)
      stream.readinto(yuv)  # stream -> YUV buffer
      stream.close()
      yuv2rgb.convert(yuv, rgb, 480,320)

      connection.sendall(rgb[0:(480 * 320 * 3)])
      time.sleep(0.1)
      connection.close()
except:
   print 'Closing'
   camera.close()
finally:
   print 'closing'
   camera.close()
