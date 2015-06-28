GoPiGo for Node.js
=======

The GoPiGo is a delightful and complete robot for the Raspberry Pi that turns your Pi into a fully operating robot.  GoPiGo is a mobile robotic platform for the Raspberry Pi developed by [Dexter Industries.](http://www.dexterindustries.com/GoPiGo)

![ GoPiGo ](https://raw.githubusercontent.com/DexterInd/GoPiGo/master/GoPiGo_Chassis-300.jpg)

#License

This project is open source.  These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.

## Quick start

Before to start you should install Node.js on your RaspberryPi and clone the repo on your local environment.
Be sure to have npm installed and then you can proceed installing the package.

Go inside your Node.js application folder and type
```bash
$ npm install node-gopigo
```

Now you can include the module inside your application as usual:
```javascript
var Gopigo = require('node-gopigo')
```

At this point you may need to include the GoPiGo base classes:
```javascript
var Commands = Gopigo.commands
var Robot = Gopigo.robot
```

Now you can instanciate the GoPiGo, for example:
```javascript
robot = new Robot({
  minVoltage: 5.5,
  criticalVoltage: 1.2,
  debug: true,
  ultrasonicSensorPin: 15
})
```

The next step is to add some listeners:
```javascript
robot.on('init', function onInit(res) {
  if (res) {
    console.log('GoPiGo Ready!')
    /* Now you can do awesome stuff with your GoPiGo */
  } else {
    console.log('Something went wrong during the init.')
  }
})
robot.on('error', function onError(err) {
  console.log('Something went wrong')
  console.log(err)
})
robot.on('free', function onFree() {
  console.log('GoPiGo is free to go')
})
robot.on('halt', function onHalt() {
  console.log('GoPiGo is halted')
})
robot.on('close', function onClose() {
  console.log('GoPiGo is going to sleep')
})
robot.on('reset', function onReset() {
  console.log('GoPiGo is resetting')
})
robot.on('normalVoltage', function onNormalVoltage(voltage) {
  console.log('Voltage is ok ['+voltage+']')
})
robot.on('lowVoltage', function onLowVoltage(voltage) {
  console.log('(!!) Voltage is low ['+voltage+']')
})
robot.on('criticalVoltage', function onCriticalVoltage(voltage) {
  console.log('(!!!) Voltage is critical ['+voltage+']')
})
```

When you are ready to go you should call the init method
```javascript
robot.init()
```

You'll find a more complex example in the "basicTest.js" file under the "tests" folder of the repository.