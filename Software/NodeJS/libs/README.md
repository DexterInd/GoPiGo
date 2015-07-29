GoPiGo for Node.js
=======

The GoPiGo is a delightful and complete robot for the Raspberry Pi that turns your Pi into a fully operating robot.  GoPiGo is a mobile robotic platform for the Raspberry Pi developed by [Dexter Industries.](http://www.dexterindustries.com/GoPiGo)

![ GoPiGo ](https://raw.githubusercontent.com/DexterInd/GoPiGo/master/GoPiGo_Chassis-300.jpg)

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