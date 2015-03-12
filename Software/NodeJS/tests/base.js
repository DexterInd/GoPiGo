var gopigo   = require('../gopigo')
var readline = require('readline')
var sleep = require('sleep')

var ultrasonic_pin = 15

var rl = readline.createInterface({
  input : process.stdin,
  output: process.stdout
});

console.log(' Welcome to the GoPiGo test application             ')
console.log(' When asked, insert a command to test your GoPiGo   ')
console.log(' (!) For a complete list of commands, please type help')

gopigo.init({
  debug: true,
  reset: true,
  minVoltage: 5.5,
  sensors: {
    'ultrasonic': ultrasonic_pin
  },
  onInit: function callback() {
    console.log('GoPiGo Ready!')
    askForCommand()
  },
  onLowVoltage: function callback(res) {
    console.log('GoPiGo has detected a low voltage ('+res+' V). You probably shut down the system securely in order to avoid issues.')
  },
  onError: function(err) {
    console.log('Something went wrong')
    console.log(err)
  }
})

function askForCommand() {
  rl.question('What do you want me to do? > ', function(answer) {
    handleAnswer(answer)
  })
}

function handleAnswer(answer) {
  var message = ''
  switch (answer) {
    case 'help':
      console.log('')
      console.log('reset => performs a reset of LEDs and servo motor')
      console.log('left led on => turn left led on')
      console.log('left led off => turn left led off')
      console.log('right led on => turn right led on')
      console.log('right led off => turn right led off')
      console.log('move forward => moves the GoPiGo forward')
      console.log('move backward => moves the GoPiGo backward')
      console.log('turn left => turns the GoPiGo to the left')
      console.log('turn right => turns the GoPiGo to the right')
      console.log('stop => stops the GoPiGo')
      console.log('increase speed => increases the motors speed')
      console.log('decrease speed => decreases the motors speed')
      console.log('voltage => returns the voltage value')
      console.log('servo test => performs a servo test')
      console.log('ultrasonic distance => returns the distance from an object')
      console.log('move forward with PID => moves the GoPiGo forward with PID')
      console.log('move backward with PID => moves the GoPiGo backward with PID')
      console.log('rotate left => rotates the GoPiGo to the left')
      console.log('rotate right => rotates the GoPiGo to the right')
      console.log('set encoder targeting => sets the encoder targeting')
      console.log('firmware version => returns the firmware version')
      console.log('exit => exits from this test')
      console.log('')
    break
    case 'reset':
      gopigo.reset()
    break
    case 'left led on':
      gopigo.led_on(gopigo.LED_L_PIN, function onLedOn(res) {
        console.log('Led left on::'+res)
      })
    break
    case 'left led off':
      gopigo.led_off(gopigo.LED_L_PIN, function onLedOff(res) {
        console.log('Led left off::'+res)
      })
    break
    case 'right led on':
      gopigo.led_on(gopigo.LED_R_PIN, function onLedOn(res) {
        console.log('Led right on::'+res)
      })
    break
    case 'right led off':
      gopigo.led_off(gopigo.LED_R_PIN, function onLedOff(res) {
        console.log('Led right off::'+res)
      })
    break
    case 'move forward':
    case 'w':
      gopigo.forward(function onTestComplete(res) {
        console.log('Moving forward::' + res)
      }, false)
    break
    case 'turn left':
    case 'a':
      gopigo.left(function onTestComplete(res) {
        console.log('Turning left::' + res)
      })
    break
    case 'turn right':
    case 'd':
      gopigo.right(function onTestComplete(res) {
        console.log('Turning right::' + res)
      })
    break
    case 'move backward':
    case 's':
      gopigo.backward(function onTestComplete(res) {
        console.log('Moving backward::' + res)
      }, false)
    break
    case 'stop':
    case 'x':
      gopigo.stop(function onTestComplete(res) {
        console.log('Stop::' + res)
      })
    break
    case 'increase speed':
    case 't':
      gopigo.increase_speed(function onTestComplete(res) {
        console.log('Increasing speed::' + res)
      })
    break
    case 'decrease speed':
    case 'g':
      gopigo.decrease_speed(function onTestComplete(res) {
        console.log('Decreasing speed::' + res)
      })
    break
    case 'voltage':
    case 'v':
      gopigo.volt(function onTestComplete(res) {
        console.log('Voltage::' + res + ' V')
      })
    break
    case 'servo test':
    case 'b':
      gopigo.servo(0, function onTestComplete(res) {
        console.log('servo in position 0')

        sleep.sleep(1)
        gopigo.servo(180, function onTestComplete(res) {
          console.log('servo in position 180')

          sleep.sleep(1)
          gopigo.servo(90, function onTestComplete(res) {
            console.log('servo in position 90')
          })
        })
      })
    break
    case 'exit':
    case 'z':
      process.exit()
    break
    case 'ultrasonic distance':
    case 'u':
      gopigo.ultrasonic_distance(ultrasonic_pin, function onTestComplete(res) {
        console.log('Ultrasonic Distance::' + res + ' cm')
      })
    break
    case 'l':
      // TODO
    break
    case 'move forward with pid':
    case 'i':
      gopigo.forward(function onTestComplete(res) {
        console.log('Moving forward::' + res)
      }, true)
    break
    case 'move backward with pid':
    case 'k':
      gopigo.backward(function onTestComplete(res) {
        console.log('Moving forward::' + res)
      }, true)
    break
    case 'rotate left':
    case 'n':
      gopigo.left_with_rotation(function onTestComplete(res) {
        console.log('Rotating left::' + res)
      })
    break
    case 'rotate right':
    case 'm':
      gopigo.right_with_rotation(function onTestComplete(res) {
        console.log('Rotating right::' + res)
      })
    break
    case 'set encoder targeting':
    case 'y':
      gopigo.encoder_targeting(1, 1, 18, function onTestComplete(res) {
        console.log('Setting encoder targeting:1:1:18::' + res)
      })
    break
    case 'firmware version':
    case 'f':
      gopigo.version(function onTestComplete(res) {
        console.log('Firmware version::' + res)
      })
    break
  }

  sleep.sleep(1)
  askForCommand()
}