#!/usr/bin/python

import gopigo
try:
    import wx
except ImportError:
    raise ImportError,"The wxPython module is required to run this program"

import atexit
atexit.register(gopigo.stop)    

left_led=0
right_led=0
trim_val=gopigo.trim_read()
v=gopigo.volt()
f=gopigo.fw_ver()
slider_val=gopigo.trim_read()

class gopigo_control_app(wx.Frame):
    slider=0
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self,parent,id,title,size=(475,600))
        self.parent = parent
        self.initialize()
        # Exit
        exit_button = wx.Button(self, label="Exit", pos=(240+75,550))
        exit_button.Bind(wx.EVT_BUTTON, self.onClose)
        
        # robot = "/home/pi/Desktop/GoBox/Troubleshooting_GUI/dex.png"
        # png = wx.Image(robot, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        # wx.StaticBitmap(self, -1, png, (0, 0), (png.GetWidth()-320, png.GetHeight()-20))
        # self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)		# Sets background picture
    
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
        # bmp = wx.Bitmap("/home/pi/Desktop/GoBox/Troubleshooting_GUI/dex.png")	# Draw the photograph.
        # dc.DrawBitmap(bmp, 0, 400)						# Absolute position of where to put the picture


    def initialize(self):
        sizer = wx.GridBagSizer()
        
        # Motion buttons
        x=75
        y=175 
        dist=60
       
        left_button = wx.Button(self,-1,label="Left", pos=(x,y))
        sizer.Add(left_button, (0,1))
        self.Bind(wx.EVT_BUTTON, self.left_button_OnButtonClick, left_button)

        stop_button = wx.Button(self,-1,label="Stop", pos=(x+dist*2,y))
        sizer.Add(stop_button, (0,1))
        self.Bind(wx.EVT_BUTTON, self.stop_button_OnButtonClick, stop_button)

        right_button = wx.Button(self,-1,label="Right", pos=(x+dist*4,y))
        sizer.Add(right_button, (0,1))
        self.Bind(wx.EVT_BUTTON, self.right_button_OnButtonClick, right_button)
        
        fwd_button = wx.Button(self,-1,label="Forward", pos=(x+dist*2,y-dist))
        sizer.Add(fwd_button, (0,1))
        self.Bind(wx.EVT_BUTTON, self.fwd_button_OnButtonClick, fwd_button)
        
        bwd_button = wx.Button(self,-1,label="Back", pos=(x+dist*2,y+dist))
        sizer.Add(bwd_button, (0,1))
        self.Bind(wx.EVT_BUTTON, self.bwd_button_OnButtonClick, bwd_button)
        
        # Led buttons
        x=75
        y=25
        left_led_button = wx.Button(self,-1,label="Left LED", pos=(x,y))
        sizer.Add(left_led_button, (0,1))
        self.Bind(wx.EVT_BUTTON, self.left_led_button_OnButtonClick, left_led_button)

        right_led_button = wx.Button(self,-1,label="Right LED", pos=(x+dist*4,y))
        sizer.Add(right_led_button, (0,1))
        self.Bind(wx.EVT_BUTTON, self.right_led_button_OnButtonClick, right_led_button)        
        
        y=320
        battery_button = wx.Button(self,-1,label="  Battery Voltage\t  ", pos=(x,y))
        sizer.Add(battery_button, (0,1))
        self.Bind(wx.EVT_BUTTON, self.battery_button_OnButtonClick, battery_button)

        firmware_button = wx.Button(self,-1,label="Firmware version ", pos=(x,y+dist/2))
        sizer.Add(firmware_button, (0,1))
        self.Bind(wx.EVT_BUTTON, self.firmware_button_OnButtonClick, firmware_button)        
        # Set up labels
        # self.label = wx.StaticText(self,-1,label=u'  ',pos=(25,y+150))       
        # self.label_top = wx.StaticText(self,-1,label=u'Test',pos=(25,0))
        # sizer.Add( self.label, (1,0),(1,2), wx.EXPAND )
        # sizer.Add( self.label_top, (1,0),(1,2), wx.EXPAND )
        
        self.battery_label = wx.StaticText(self,-1,label=str(v)+"V",pos=(x+dist*2,y+6))
        sizer.Add( self.battery_label, (1,0),(1,2), wx.EXPAND )
        
        self.firmware_label = wx.StaticText(self,-1,label=str(f),pos=(x+dist*2,y+6+dist/2))
        sizer.Add( self.firmware_label, (1,0),(1,2), wx.EXPAND )
        
        
        y=420
        self.trim_label = wx.StaticText(self,-1,label=str(trim_val),pos=(x+dist*2,y+6))
        sizer.Add( self.trim_label, (1,0),(1,2), wx.EXPAND )
        
        trim_read_button = wx.Button(self,-1,label="  Trim Read ", pos=(x,y))
        sizer.Add(trim_read_button, (0,1))
        self.Bind(wx.EVT_BUTTON, self.trim_read_button_OnButtonClick, trim_read_button)

        trim_test_button = wx.Button(self,-1,label="Trim Test ", pos=(x,y+dist/2))
        sizer.Add(trim_test_button, (0,1))
        self.Bind(wx.EVT_BUTTON, self.trim_test_button_OnButtonClick, trim_test_button)
        
        trim_write_button = wx.Button(self,-1,label="Trim Write", pos=(x,y+dist))
        sizer.Add(trim_write_button, (0,1))
        self.Bind(wx.EVT_BUTTON, self.trim_write_button_OnButtonClick, trim_write_button)
        
        self.slider = wx.Slider(self, value=0, minValue=-100, maxValue=100, pos=(x+dist*2, y+dist/2),size=(250, -1), style=wx.SL_HORIZONTAL)
        self.slider.Bind(wx.EVT_SCROLL, self.OnSliderScroll)
        
        self.Show(True)     

    def battery_button_OnButtonClick(self,event):
        global v
        v=gopigo.volt()
        self.battery_label.SetLabel(str(v)+"V")    
        
    def firmware_button_OnButtonClick(self,event):
        global f
        f=gopigo.fw_ver()
        self.firmware_label.SetLabel(str(f))
     
    def left_button_OnButtonClick(self,event):
        f=gopigo.left()
 
    def stop_button_OnButtonClick(self,event):
        f=gopigo.stop()

    def right_button_OnButtonClick(self,event):
        f=gopigo.right()
        
    def fwd_button_OnButtonClick(self,event):
        f=gopigo.fwd()

    def bwd_button_OnButtonClick(self,event):
        f=gopigo.bwd()  

    def left_led_button_OnButtonClick(self,event):
        global left_led
        if left_led==0:
            gopigo.led_on(1)
            left_led=1        
        else :
            gopigo.led_off(1)
            left_led=0
    
    def right_led_button_OnButtonClick(self,event):
        global right_led
        if right_led==0:
            gopigo.led_on(0)
            right_led=1        
        else :
            gopigo.led_off(0)
            right_led=0
            
    def trim_read_button_OnButtonClick(self,event):
        trim_val=gopigo.trim_read()
        if trim_val==-3:
            trim==0
        else:
            trim_val=trim_val-100
        self.slider.SetValue(trim_val)
        self.trim_label.SetLabel(str(trim_val))
        
    def trim_test_button_OnButtonClick(self,event):
        global slider_val
        gopigo.trim_test(slider_val)

    def trim_write_button_OnButtonClick(self,event):
        global slider_val
        gopigo.trim_write(slider_val)
            
    def OnSliderScroll(self,event):
        global slider_val
        obj = event.GetEventObject()
        slider_val = obj.GetValue()
        self.trim_label.SetLabel(str(slider_val))
        
    def onClose(self, event):	# Close the entire program.
        self.Close()

if __name__ == "__main__":
    app = wx.App()
    frame = gopigo_control_app(None,-1,'GoPiGo Control Panel')
    app.MainLoop()