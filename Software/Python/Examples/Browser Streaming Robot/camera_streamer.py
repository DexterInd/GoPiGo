#!/usr/bin/env python
##############################################################################################################                                                              
# This example is for streaming video and controlling the GoPiGo from a web browser
# http://www.dexterindustries.com/GoPiGo/                                                                
# History
# ------------------------------------------------
# Author     Date      		Comments
# Karan      24 July 14  	Initial Authoring                                                          
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)           
#
# This example is derived from the Dawn Robotics Raspberry Pi Camera Bot
# https://bitbucket.org/DawnRobotics/raspberry_pi_camera_bot
#############################################################################################################

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

import copy
import os
import os.path
import subprocess
import time
import logging

#---------------------------------------------------------------------------------------------------
class CameraStreamer:
    
    """A class to look after streaming images from the Raspberry Pi camera.
       Ideally, the camera should only be on when somebody wants to stream images.
       Therefore, startStreaming must be called periodically. If startStreaming
       is not called before a timeout period expires then the streaming will stop"""

    DEFAULT_TIMEOUT = 4.0
    
    #-----------------------------------------------------------------------------------------------
    def __init__( self, timeout=DEFAULT_TIMEOUT ):
            
        self.cameraStreamerProcess = None
        self.streamingStartTime = 0
        self.streamingTimeout = timeout

    #-----------------------------------------------------------------------------------------------
    def __del__( self ):

        self.stopStreaming()
        
    #-----------------------------------------------------------------------------------------------
    def startStreaming( self ):
        
        # Start raspberry_pi_camera_streamer if needed
        if self.cameraStreamerProcess == None or self.cameraStreamerProcess.poll() != None:
            
            self.cameraStreamerProcess = subprocess.Popen( 
                [ "/usr/local/bin/raspberry_pi_camera_streamer" ] )
        
        self.streamingStartTime = time.time()         
                
    #-----------------------------------------------------------------------------------------------
    def update( self ):
        
        if time.time() - self.streamingStartTime > self.streamingTimeout:
            
            self.stopStreaming()
                
    #-----------------------------------------------------------------------------------------------
    def stopStreaming( self ):

        if self.cameraStreamerProcess != None:
            self.cameraStreamerProcess.terminate()
