#!/usr/bin/python

try:
    import wx
except ImportError:
    raise ImportError,"The wxPython module is required to run this program"

try:
    import sys
    sys.path.insert(0, '/home/pi/Desktop/GoPiGo/Software/Python/line_follower')

    import line_sensor
    import scratch_line
except ImportError:
    raise ImportError,"Line sensor libraries not found"
  
y=175 
class line_sensor_app(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self,parent,id,title,size=(475,400))
        self.parent = parent
        self.initialize()
        # Exit
        exit_button = wx.Button(self, label="Exit", pos=(25,350))
        exit_button.Bind(wx.EVT_BUTTON, self.onClose)
        
        robot = "/home/pi/Desktop/GoBox/Troubleshooting_GUI/dex.png"
        png = wx.Image(robot, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        wx.StaticBitmap(self, -1, png, (395, 275), (png.GetWidth()-320, png.GetHeight()-10))
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)		# Sets background picture
    
    #----------------------------------------------------------------------
    def OnEraseBackground(self, evt):
        """
        Add a picture to the background
        """
        # yanked from ColourDB.py
        dc = evt.GetDC()
 
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()	
        bmp = wx.Bitmap("/home/pi/Desktop/GoBox/Troubleshooting_GUI/dex.png")	# Draw the photograph.
        dc.DrawBitmap(bmp, 0, 400)						# Absolute position of where to put the picture


    def initialize(self):
        sizer = wx.GridBagSizer()

        # Set up buttons
        black_line_set_button = wx.Button(self,-1,label="Set Black Line Values", pos=(25,y))
        sizer.Add(black_line_set_button, (0,1))
        self.Bind(wx.EVT_BUTTON, self.black_line_set_OnButtonClick, black_line_set_button)

        white_line_set_button = wx.Button(self,-1,label="Set White Line Values", pos=(175,y))
        sizer.Add(white_line_set_button, (0,1))
        self.Bind(wx.EVT_BUTTON, self.white_line_set_button_OnButtonClick, white_line_set_button)

        line_position_set_button = wx.Button(self,-1,label="Read Line Position", pos=(325,y))
        sizer.Add(line_position_set_button, (0,1))
        self.Bind(wx.EVT_BUTTON, self.line_position_set_button_OnButtonClick, line_position_set_button)
        
        # Set up labels
        self.label = wx.StaticText(self,-1,label=u'  ',pos=(25,y+150))
        
        self.label_top = wx.StaticText(self,-1,label=u'Instructions:\n 1.\tPlace the line sensor so that all of the black sensors are over \n\tyour black line.  Then press the button "Black Line Sensor Set".\n\n 2.\tNext, place the line sensor so that all of the black sensors are \n\tNOT over your black line and on the white background surface.\n\tThen press "White Line Sensor Set".\n\n 3.\tFinally, test the sensor by pressing "Read Line Position"',pos=(25,0))

        sizer.Add( self.label, (1,0),(1,2), wx.EXPAND )
        sizer.Add( self.label_top, (1,0),(1,2), wx.EXPAND )

        self.Show(True)

    def black_line_set_OnButtonClick(self,event):
        for i in range(2):
            line_sensor.get_sensorval()
        line_sensor.set_black_line()
        line_val=line_sensor.get_black_line()
        self.label.SetLabel("Black Line : "+str(line_val))
        
	
    def white_line_set_button_OnButtonClick(self,event):
        for i in range(2):
            line_sensor.get_sensorval()
        line_sensor.set_white_line()
        line_val=line_sensor.get_white_line()
        self.label.SetLabel("White Line : "+str(line_val))
        
    def line_position_set_button_OnButtonClick(self,event):
        line_val=scratch_line.absolute_line_pos()
        self.label.SetLabel("Line Position : "+str(line_val))

    def onClose(self, event):	# Close the entire program.
        self.Close()

if __name__ == "__main__":
    app = wx.App()
    frame = line_sensor_app(None,-1,'Line Follower Calibration')
    app.MainLoop()
