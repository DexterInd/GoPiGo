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
    
class line_sensor_app(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self,parent,id,title,size=(400,300))
        self.parent = parent
        self.initialize()

    def initialize(self):
        sizer = wx.GridBagSizer()

        # Set up buttons
        black_line_set_button = wx.Button(self,-1,label="Black Line sensor set", pos=(25,75))
        sizer.Add(black_line_set_button, (0,1))
        self.Bind(wx.EVT_BUTTON, self.black_line_set_OnButtonClick, black_line_set_button)

        white_line_set_button = wx.Button(self,-1,label="White Line sensor set", pos=(25,125))
        sizer.Add(white_line_set_button, (0,1))
        self.Bind(wx.EVT_BUTTON, self.white_line_set_button_OnButtonClick, white_line_set_button)

        line_position_set_button = wx.Button(self,-1,label="Read Line Position", pos=(25,175))
        sizer.Add(line_position_set_button, (0,1))
        self.Bind(wx.EVT_BUTTON, self.line_position_set_button_OnButtonClick, line_position_set_button)
        
        # Set up labels
        self.label = wx.StaticText(self,-1,label=u'Hello !',pos=(25,225))
        
        self.label_top = wx.StaticText(self,-1,label=u'LINE SENSOR SETUP !\nKeep the line sensor over white and black line \nand select the button to set the treshold',pos=(25,0))

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


if __name__ == "__main__":
    app = wx.App()
    frame = line_sensor_app(None,-1,'Line Follower setup')
    app.MainLoop()
