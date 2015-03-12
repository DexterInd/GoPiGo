GoPiGo for Node.js
=======

The GoPiGo is a delightful and complete robot for the Raspberry Pi that turns your Pi into a fully operating robot.  GoPiGo is a mobile robotic platform for the Raspberry Pi developed by [Dexter Industries.](http://www.dexterindustries.com/GoPiGo)  

![ GoPiGo ](https://raw.githubusercontent.com/DexterInd/GoPiGo/master/GoPiGo_Chassis-300.jpg)

#License

This project is open source.  These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.

## Table of contents

- [Quick start](#quick-start)
- [Conclusions](#conclusions)

## Quick start

Before to start you should install Node.js on your RaspberryPi and clone the repo on your local environment. 
Be sure to have npm installed and then you can proceed installing the package.

Go inside your Node.js application folder and type
```bash
$ npm install node-gopigo
```
Now you can include the module inside your application as usual:
```javascript
var gopigo = require('node-gopigo')
```

Once the module has been loaded you can start using it:
```javascript
gopigo.init({
  reset: true,
  sensors: {
    'ultrasonic': 15
  },
  minVoltage: 5.5,
  onInit: function callback() {
    console.log('GoPiGo Ready!')
    gopigo.forward(function onForward(res) {
      console.log('Moving forward::' + res)
    })
  },
  onLowVoltage: function callback(res) {
    console.log('GoPiGo has detected a low voltage ('+res+' V). You probably shut down the system securely in order to avoid issues.')
  },
  onError: function(err) {
    console.log('Something went wrong')
    console.log(err)
  }
})
```

* The "sensors" object defines the attached sensors and the relative pins
* The "reset" option will reset the servo's position and the leds' status after the init.
* The "onLowVoltage" callback will be invoked in case of the voltage drops under 5.5 Volts (default value) or the preferred value passed through the "minVoltage" parameter

## Conclusions
A lot of improvements are waiting to be implemented so be patient and stay focused! :-)