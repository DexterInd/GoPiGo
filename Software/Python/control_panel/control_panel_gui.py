#!/usr/bin/python

# try to import the auto_detection library
try:
    import auto_detect_robot
    no_auto_detect = False
except:
    no_auto_detect = True

import gopigo
try:
    import wx
except ImportError:
    raise ImportError,"The wxPython module is required to run this program"

import atexit
atexit.register(gopigo.stop)

left_led = 0
right_led = 0
trim_val = gopigo.trim_read()
if trim_val == -3:
    trim_val = 0
v = gopigo.volt()
f = gopigo.fw_ver()
slider_val = trim_val

class MainPanel(wx.Panel):
    slider=0
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(wx.WHITE)
        self.frame = parent

        # main sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.AddSpacer(10)

        # if we can auto-detect, then give feedback to the user
        if no_auto_detect == False:
            detected_robot = auto_detect_robot.autodetect()
            if detected_robot != "GoPiGo":
                detected_robot_str = wx.StaticText(self,-1,
                    label="Warning: Could not find a GoPiGo")
                detected_robot_str.SetForegroundColour('red')
                warning_sizer = wx.BoxSizer(wx.HORIZONTAL)
                warning_sizer.Add(detected_robot_str, 0, wx.EXPAND| wx.ALIGN_CENTER)
                main_sizer.Add(warning_sizer, 0, wx.ALIGN_CENTER)

        # LED buttons
        led_sizer = wx.BoxSizer(wx.HORIZONTAL)

        left_led_button = wx.Button(self, label="Left LED")
        self.Bind(wx.EVT_BUTTON, self.left_led_button_OnButtonClick, left_led_button)

        right_led_button = wx.Button(self, label="Right LED")
        self.Bind(wx.EVT_BUTTON, self.right_led_button_OnButtonClick, right_led_button)       

        led_sizer.AddSpacer(30)
        led_sizer.Add(left_led_button, 0, wx.ALIGN_CENTER)
        led_sizer.AddSpacer(80)
        led_sizer.Add(right_led_button, 0, wx.ALIGN_CENTER)
        led_sizer.AddSpacer(30)


        fwd_sizer = wx.BoxSizer(wx.HORIZONTAL)
        fwd_button = wx.Button(self, label="Forward")
        self.Bind(wx.EVT_BUTTON, self.fwd_button_OnButtonClick, fwd_button)
        fwd_sizer.Add(fwd_button, 0, wx.ALIGN_CENTER)

        middle_sizer = wx.BoxSizer(wx.HORIZONTAL)
        left_button = wx.Button(self, label="Left")
        self.Bind(wx.EVT_BUTTON, self.left_button_OnButtonClick, left_button)
        stop_button = wx.Button(self, label="Stop")
        stop_button.SetBackgroundColour('red')
        self.Bind(wx.EVT_BUTTON, self.stop_button_OnButtonClick, stop_button)
        right_button = wx.Button(self, label="Right")
        self.Bind(wx.EVT_BUTTON, self.right_button_OnButtonClick, right_button)

        middle_sizer.Add(left_button, 0, wx.ALIGN_CENTER)
        middle_sizer.AddSpacer(20)
        middle_sizer.Add(stop_button,  0, wx.ALIGN_CENTER)
        middle_sizer.AddSpacer(20)
        middle_sizer.Add(right_button,  0, wx.ALIGN_CENTER)
        
        bwdSizer = wx.BoxSizer(wx.HORIZONTAL)
        bwd_button = wx.Button(self, label="Back")
        self.Bind(wx.EVT_BUTTON, self.bwd_button_OnButtonClick, bwd_button)
        bwdSizer.Add(bwd_button,  0, wx.ALIGN_CENTER)

        batterySizer = wx.BoxSizer(wx.HORIZONTAL)
        battery_button = wx.Button(self, label="Check Battery Voltage")
        self.Bind(wx.EVT_BUTTON, self.battery_button_OnButtonClick, battery_button)
        self.battery_label = wx.StaticText(self, label=str(round(v,1))+"V")
        batterySizer.AddSpacer(30)
        batterySizer.Add(battery_button, 0, wx.ALIGN_LEFT )
        batterySizer.AddSpacer(20)
        batterySizer.Add( self.battery_label,0, wx.ALIGN_CENTER|wx.EXPAND )

        firmwareSizer = wx.BoxSizer(wx.HORIZONTAL)
        firmware_button = wx.Button(self,-1,label="Check Firmware Version")
        self.Bind(wx.EVT_BUTTON, self.firmware_button_OnButtonClick, firmware_button)        
        self.firmware_label = wx.StaticText(self,-1,label=str(f))
        firmwareSizer.AddSpacer(30)
        firmwareSizer.Add(firmware_button, 0, wx.ALIGN_LEFT)
        firmwareSizer.AddSpacer(15)
        firmwareSizer.Add( self.firmware_label, 0, wx.ALIGN_CENTER|wx.EXPAND )

        trimbuttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        trim_read_button = wx.Button(self, label="  Trim Read ")
        self.Bind(wx.EVT_BUTTON, self.trim_read_button_OnButtonClick, trim_read_button)
        trim_test_button = wx.Button(self, label="Trim Test ")
        self.Bind(wx.EVT_BUTTON, self.trim_test_button_OnButtonClick, trim_test_button)
        trim_write_button = wx.Button(self, label="Trim Write")
        self.Bind(wx.EVT_BUTTON, self.trim_write_button_OnButtonClick, trim_write_button)

        # trimbuttons_sizer.AddSpacer(30)
        trimbuttons_sizer.Add( trim_read_button, 0, wx.ALIGN_CENTER )
        trimbuttons_sizer.AddSpacer(30)
        trimbuttons_sizer.Add( trim_test_button, 0,  wx.ALIGN_CENTER)
        trimbuttons_sizer.AddSpacer(30)
        trimbuttons_sizer.Add( trim_write_button, 0,  wx.ALIGN_CENTER )

        trim_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.trim_label = wx.StaticText(self, -1, label="Trim: "+str(trim_val))
        self.slider = wx.Slider(self, value=0, minValue=-100, maxValue=100, size=(250, -1), style=wx.SL_HORIZONTAL)
        self.slider.Bind(wx.EVT_SCROLL, self.OnSliderScroll)

        trim_sizer.Add( self.trim_label, 0, wx.ALIGN_CENTER )
        trim_sizer.AddSpacer(30)
        trim_sizer.Add( self.slider, 0, wx.ALIGN_CENTER )

        # Exit
        exit_sizer = wx.BoxSizer(wx.HORIZONTAL)
        exit_button = wx.Button(self, label="Exit")
        exit_button.Bind(wx.EVT_BUTTON, self.onClose)
        exit_sizer.Add(exit_button,0, wx.ALIGN_RIGHT)
        exit_sizer.AddSpacer(30)


        main_sizer.Add(led_sizer, 0,  wx.ALIGN_CENTER)
        main_sizer.AddSpacer(10)
        main_sizer.Add(fwd_sizer, 0,  wx.ALIGN_CENTER)
        main_sizer.AddSpacer(10)
        main_sizer.Add(middle_sizer, 0,  wx.ALIGN_CENTER)
        main_sizer.AddSpacer(10)
        main_sizer.Add(bwdSizer, 0,  wx.ALIGN_CENTER)
        main_sizer.AddSpacer(40)
        main_sizer.Add(trimbuttons_sizer, 0, wx.ALIGN_CENTER)
        main_sizer.AddSpacer(5)
        main_sizer.Add(trim_sizer, 0, wx.ALIGN_CENTER)
        main_sizer.AddSpacer(30)
        main_sizer.Add(batterySizer, 0)
        main_sizer.Add(firmwareSizer, 0)
        main_sizer.AddSpacer(20)
        main_sizer.Add(exit_sizer, 0, wx.ALIGN_RIGHT)
        
        self.SetSizerAndFit(main_sizer)

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
        global trim_val
        trim_val=gopigo.trim_read()
        if trim_val == -3:
            trim_val = 0
        else:
            trim_val = trim_val-100
        self.slider.SetValue(trim_val)
        self.trim_label.SetLabel("Trim: "+str(trim_val))
        
    def trim_test_button_OnButtonClick(self,event):
        global slider_val
        gopigo.trim_test(slider_val)

    def trim_write_button_OnButtonClick(self,event):
        global slider_val
        gopigo.trim_write(slider_val)
            
    def OnSliderScroll(self, event):
        global slider_val
        obj = event.GetEventObject()
        slider_val = obj.GetValue()
        self.trim_label.SetLabel("Trim: "+str(slider_val))
        
    def onClose(self, event):	# Close the entire program.
        self.frame.Close()

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Log.SetVerbose(False)
        wx.Frame.__init__(self, None, title='GoPiGo Control Panel', size=(475,550))
        panel = MainPanel(self)
        self.Center()

class Main(wx.App):
    def __init__(self, redirect=False, filename=None):
        """Constructor"""
        wx.App.__init__(self, redirect, filename)
        dlg = MainFrame()
        dlg.Show()

if __name__ == "__main__":
    app = Main()
    app.MainLoop()