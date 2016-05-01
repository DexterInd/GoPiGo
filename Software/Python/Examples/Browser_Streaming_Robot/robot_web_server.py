#! /usr/bin/env python
##############################################################################################################                                                              
# This example is for streaming video and controlling the GoPiGo from a web browser
# http://www.dexterindustries.com/GoPiGo/                                                                
# History
# ------------------------------------------------
# Author     Date      		Comments
# Karan      24 July 14  	Initial Authoring                                                          
'''
## License
 GoPiGo for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
 Copyright (C) 2015  Dexter Industries

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
'''
#
# This example is derived from the Dawn Robotics Raspberry Pi Camera Bot
# https://bitbucket.org/DawnRobotics/raspberry_pi_camera_bot
############################################################################################################

# Copyright (c) 2014, Dawn Robotics Ltd
# All rights reserved.

# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice, 
# this list of conditions and the following disclaimer in the documentation 
# and/or other materials provided with the distribution.

# 3. Neither the name of the Dawn Robotics Ltd nor the names of its contributors 
# may be used to endorse or promote products derived from this software without 
# specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import logging

LOG_FILENAME = "/tmp/robot_web_server_log.txt"
file_location = "/home/pi/Desktop/GoPiGo/Software/Python/Examples/Browser_Streaming_Robot/www/"
logging.basicConfig( filename=LOG_FILENAME, level=logging.DEBUG )

# Also log to stdout
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel( logging.DEBUG )
logging.getLogger( "" ).addHandler( consoleHandler )

import os.path
import math
import time
import signal
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.escape
import sockjs.tornado
import threading
import Queue
import camera_streamer
import robot_controller
import json
import gopigo
import subprocess
import sys
robot = None

cameraStreamer = None
scriptPath = os.path.dirname( __file__ )
webPath = os.path.abspath( file_location)
print webPath
robotConnectionResultQueue = Queue.Queue()
isClosing = False

#--------------------------------------------------------------------------------------------------- 
def createRobot(resultQueue ):
    
    r = robot_controller.RobotController( )
    resultQueue.put( r )
            
#--------------------------------------------------------------------------------------------------- 
class ConnectionHandler( sockjs.tornado.SockJSConnection ):
    
    #-----------------------------------------------------------------------------------------------
    def on_open( self, info ):
        
        pass
        
    #-----------------------------------------------------------------------------------------------
    def on_message( self, message ):
                
        try:
            message = str( message )
        except Exception:
            logging.warning( "Got a message that couldn't be converted to a string" )
            return

        if isinstance( message, str ):
            
            lineData = message.split( " " )
            if len( lineData ) > 0:
                
                if lineData[ 0 ] == "Centre":
                
                    if robot != None:
                        robot.centreNeck()
                
                elif lineData[ 0 ] == "StartStreaming":
                    cameraStreamer.startStreaming()
                    
                elif lineData[ 0 ] == "Shutdown":
                    cameraStreamer.stopStreaming()
                    gopigo.stop()
                    robot.disconnect()
                    sys.exit()
                
                elif lineData[ 0 ] == "Move" and len( lineData ) >= 3:
                    
                    motorJoystickX, motorJoystickY = \
                        self.extractJoystickData( lineData[ 1 ], lineData[ 2 ] )
                    
                    if robot != None:
                        robot.setMotorJoystickPos( motorJoystickX, motorJoystickY )     
                elif lineData[ 0 ] == "PanTilt" and len( lineData ) >= 3:
                    
                    neckJoystickX, neckJoystickY = \
                        self.extractJoystickData( lineData[ 1 ], lineData[ 2 ] )
                        
                    if robot != None:
                        robot.setNeckJoystickPos( neckJoystickX, neckJoystickY )
                        
    #-----------------------------------------------------------------------------------------------
    def on_close( self ):
        logging.info( "SockJS connection closed" )

    def extractJoystickData( self, dataX, dataY ):
        
        joystickX = 0.0
        joystickY = 0.0
        
        try:
            joystickX = float( dataX )
        except Exception:
            pass
        
        try:
            joystickY = float( dataY )
        except Exception:
            pass
            
        return ( joystickX, joystickY )

#--------------------------------------------------------------------------------------------------- 
class MainHandler( tornado.web.RequestHandler ):
    
    #------------------------------------------------------------------------------------------------
    def get( self ):
        self.render( webPath + "/index.html" )
        
#--------------------------------------------------------------------------------------------------- 
def robotUpdate():
    
    global robot
    global isClosing
    
    if isClosing:
        tornado.ioloop.IOLoop.instance().stop()
        return
        
    if robot == None:
        
        if not robotConnectionResultQueue.empty():
            
            robot = robotConnectionResultQueue.get()
        
    else:
                
        robot.update()

#--------------------------------------------------------------------------------------------------- 
def signalHandler( signum, frame ):
    
    if signum in [ signal.SIGINT, signal.SIGTERM ]:
        global isClosing
        isClosing = True
        
        
#--------------------------------------------------------------------------------------------------- 
if __name__ == "__main__":
    
    signal.signal( signal.SIGINT, signalHandler )
    signal.signal( signal.SIGTERM, signalHandler )
    
    # Create the configuration for the web server
    router = sockjs.tornado.SockJSRouter( 
        ConnectionHandler, '/robot_control' )
    application = tornado.web.Application( router.urls + [ 
        ( r"/", MainHandler ), 
        ( r"/(.*)", tornado.web.StaticFileHandler, { "path": webPath } ),
        ( r"/css/(.*)", tornado.web.StaticFileHandler, { "path": webPath + "/css" } ),
        ( r"/css/images/(.*)", tornado.web.StaticFileHandler, { "path": webPath + "/css/images" } ),
        ( r"/images/(.*)", tornado.web.StaticFileHandler, { "path": webPath + "/images" } ),
        ( r"/js/(.*)", tornado.web.StaticFileHandler, { "path": webPath + "/js" } ) ] )
    
    #( r"/(.*)", tornado.web.StaticFileHandler, {"path": scriptPath + "/www" } ) ] \
    
    # Create a camera streamer
    cameraStreamer = camera_streamer.CameraStreamer()
    
    # Start connecting to the robot asyncronously
    robotConnectionThread = threading.Thread( target=createRobot, 
        args=[ robotConnectionResultQueue ] )
        #args=[ robotConfig, robotConnectionResultQueue ] )
    robotConnectionThread.start()

    # Now start the web server
    logging.info( "Starting web server..." )
    http_server = tornado.httpserver.HTTPServer( application )
	
	#The port number on which the robot control works, change in line 105 in www/index.html too
    http_server.listen( 98 )
    
    robotPeriodicCallback = tornado.ioloop.PeriodicCallback( 
        robotUpdate, 100, io_loop=tornado.ioloop.IOLoop.instance() )
    robotPeriodicCallback.start()
    
    cameraStreamerPeriodicCallback = tornado.ioloop.PeriodicCallback( 
        cameraStreamer.update, 1000, io_loop=tornado.ioloop.IOLoop.instance() )
    cameraStreamerPeriodicCallback.start()
    
    tornado.ioloop.IOLoop.instance().start()
    
    # Shut down code
    robotConnectionThread.join()
    
    if robot != None:
        robot.disconnect()
    else:
        if not robotConnectionResultQueue.empty():
            robot = robotConnectionResultQueue.get()
            robot.disconnect()
            
    cameraStreamer.stopStreaming()