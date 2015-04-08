var i2c         = require('i2c')
  , fs          = require('fs')
  , sleep       = require('sleep')
  , bufferTools = require('buffertools').extend()
  , async       = require('async')
  , log         = require('npmlog')
  , cmd         = require('./gopigo.commands')

  , i2c0Path  = '/dev/i2c-0'
  , i2c1Path  = '/dev/i2c-1'
  , bus, device

  , i2cCmd    = 1
  , address   = 0x08
  , bytesLen  = 4
  , trueRet   = 1                   // positive value returned by default or in case of success
  , falseRet  = -1                  // negative value returned by default (in case of errors)
  , debug     = false

  , isInit      = false
  , isHalt      = false
  , isBoardBusy = false

  , onInit = undefined
  , onLowVoltage = undefined
  , onError = undefined

  , voltageInterval      = null
  , voltageIntervalDelay = 60000    // in milliseconds (1 min.)
  , minVoltage           = 5.5      // in Volts

  , sensors = {}

  , directions = {
     'n'  : {'label': 'n' , 'degrees': 0}
   , 'ne' : {'label': 'ne', 'degrees': 45}
   , 'e'  : {'label': 'e' , 'degrees': 90}
   , 'se' : {'label': 'se', 'degrees': 135}
   , 's'  : {'label': 's' , 'degrees': 180}
   , 'sw' : {'label': 'sw', 'degrees': 225}
   , 'w'  : {'label': 'w' , 'degrees': 270}
   , 'nw' : {'label': 'nw', 'degrees': 315}
  }

var self = module.exports = {
    INPUT       : 'input'
  , OUTPUT      : 'output'
  , LED_L_PIN   : 10
  , LED_R_PIN   : 5
  , LED_L       : 1   // Led setup
  , LED_R       : 0   // Led setup
  ,
  init: function(opts) {
    if (typeof opts == 'undefined')
      opts = {}

    if (typeof opts.debug != 'undefined')
      debug = opts.debug

    if (typeof opts.sensors != 'undefined')
      sensors = opts.sensors

    if (typeof opts.minVoltage != 'undefined')
      minVoltage = opts.minVoltage

    if (typeof opts.onInit != 'undefined')
      onInit = opts.onInit

    if (typeof opts.onLowVoltage != 'undefined')
      onLowVoltage = opts.onLowVoltage

    if (typeof opts.onError !=' undefined')
      onError = opts.onError

    if (fs.existsSync(i2c0Path)) {
      isHalt = false
      device = i2c0Path
    } else if (fs.existsSync(i2c1Path)) {
      isHalt = false
      device = i2c1Path
    } else {
      var err = new Error('GoPiGo could not determine your i2c device')
      isHalt = true

      self.utils.debug(err)

      if (typeof onError == 'function') {
        onError(err)
      }
    }

    if (!isHalt) {
      bus = new i2c(address, {
        device: device
      })

      if (!isInit) {
        self.utils.debug('GoPiGo is initing')

        isInit = true

        if (typeof onLowVoltage == 'function') {
          self.utils.debug('GoPiGo will check the voltage each ' + voltageIntervalDelay + ' milliseconds')

          voltageInterval = setInterval(function onInterval() {
            self.utils.checkVoltage(onLowVoltage)
          }, voltageIntervalDelay)

          self.utils.checkVoltage(onLowVoltage)
        }

        if (opts.reset) {
          self.reset()
        }

        if (typeof onInit == 'function') {
          onInit()
        }
      }
    }
  },
  reset: function() {
    self.servo(directions.e.degrees, function onServo(){})
    self.led_off(self.LED_L_PIN, function onLedOff(){})
    self.led_off(self.LED_R_PIN, function onLedOff(){})
  },

  /*
   *
   * Private functions (should not be used directly)
   *
   */
  write_i2c_block: function(block) {
    if (!isInit || isHalt){
      if (!isHalt) {
        self.utils.debug('GoPiGo needs to be initialized.')
        return falseRet
      } else {
        return falseRet
      }
    }

    var ret = trueRet
    bus.writeBytes(i2cCmd, block, function(err) {
      isBoardBusy = false

      if (err != null) {
        self.utils.debug(err)
        return falseRet
      }
    })
    return ret
  },

  write_number: function(value) {
    if (!isInit || isHalt){
      if (!isHalt) {
        self.utils.debug('GoPiGo needs to be initialized.')
        return falseRet
      } else {
        return falseRet
      }
    }

    var ret = trueRet
    bus.writeByte(value, function(err) {
      isBoardBusy = false

      if (err != null) {
        self.utils.debug(err)
        return falseRet
      }
    })
    return ret
  },

  read_i2c_byte: function() {
    if (!isInit || isHalt){
      if (!isHalt) {
        self.utils.debug('GoPiGo needs to be initialized.')
        return falseRet
      } else {
        return falseRet
      }
    }

    return bus.readByte(function(err, res) {
      isBoardBusy = false

      if (err != null) {
        self.utils.debug(err)
        return falseRet
      } else {
        return res
      }
    })
  },

  /*
   *
   * Basic Arduino Functions
   *
   */
  pinMode: function(pin, mode) {
    if (mode == self.OUTPUT) {
      self.write_i2c_block(cmd.pMode.concat([pin, 1, cmd.unused]))
    } else if (mode == self.INPUT) {
      self.write_i2c_block(cmd.pMode.concat([pin, 0, cmd.unused]))
    }
    isBoardBusy = false
    return trueRet
  },

  digitalRead: function(pin) {
    self.write_i2c_block(cmd.dRead.concat([pin, cmd.unused, cmd.unused]))
    self.utils.wait(100)
    var val = self.read_i2c_byte()
    isBoardBusy = false
    return val
  },

  digitalWrite: function(pin, value) {
    self.write_i2c_block(cmd.dWrite.concat([pin, value, cmd.unused]))
    isBoardBusy = false
    return trueRet
  },

  analogRead: function(pin, callback, len) {
    if (typeof len == 'undefined')
      len = bytesLen

    if (typeof callback != 'function') {
      self.utils.debug('Callback is mandatory')
      return
    }

    if (!isInit || isHalt){
      if (!isHalt) {
        self.utils.debug('GoPiGo needs to be initialized.')
        callback(falseRet)
        return
      } else {
        callback(falseRet)
        return
      }
    }

    bus.writeBytes(i2cCmd, cmd.aRead.concat([pin, cmd.unused, cmd.unused]), function onBusRes(err) {
      if (err != null) {
        callback(falseRet)
        self.utils.debug(err)
        return
      }

      bus.readByte(function onReadByte(err, res) {
        if (err != null) {
          callback(falseRet)
          self.utils.debug(err)
          return
        }

        bus.readBytes(i2cCmd, len, function onReadBytes(err, res) {
          if (err) {
            self.utils.debug(err)
            callback(falseRet)
            return falseRet
          }

          callback(res[1] * 256 + res[2])
          isBoardBusy = false
          return trueRet
        })
      })
    })
  },

  analogWrite: function(pin, value) {
    self.write_i2c_block(cmd.aWrite.concat([pin, value, cmd.unused]))
    return trueRet
  },

  /*
   *
   * GoPiGo Specific functions
   *
   */
  /** Control Motor 1 **/
  moveMotorOne: function(direction, speed, callback) {
    self.write_i2c_block(cmd.m1.concat([direction, speed, cmd.unused]))
    callback(trueRet)

    return self
  },

  /** Control Motor 2 **/
  moveMotorTwo: function(direction, speed, callback) {
    self.write_i2c_block(cmd.m2.concat([direction, speed, cmd.unused]))
    callback(trueRet)

    return self
  },

  /** Move Forward **/
  forward: function(callback, usePID) {
    if (typeof usePID == 'undefined')
      usePID = false

    var _cmd = usePID ? cmd.fwd : cmd.motor_fwd

    self.write_i2c_block(_cmd.concat([cmd.unused, cmd.unused, cmd.unused]))
    callback(trueRet)

    return self
  },

  /** Move Backward **/
  backward: function(callback, usePID) {
    if (typeof usePID == 'undefined')
      usePID = false

    var _cmd = usePID ? cmd.bwd : cmd.motor_bwd

    self.write_i2c_block(_cmd.concat([cmd.unused, cmd.unused, cmd.unused]))
    callback(trueRet)

    return self
  },

  /** Turn left slowly (one motor off, better control) **/
  left: function(callback, opts) {
    if (typeof opts == 'undefined')
      opts = {}

    self.write_i2c_block(cmd.left.concat([cmd.unused, cmd.unused, cmd.unused]))
    callback(trueRet)

    return self
  },

  /** Rotate left (both motor moving in the opposite direction) **/
  left_with_rotation: function(callback, opts) {
    if (typeof opts == 'undefined')
      opts = {}

    self.write_i2c_block(cmd.left_rot.concat([cmd.unused, cmd.unused, cmd.unused]))
    callback(trueRet)

    return self
  },

  /** Turn right slowly (one motor off, better control) **/
  right: function(callback, opts) {
    if (typeof opts == 'undefined')
      opts = {}

    self.write_i2c_block(cmd.right.concat([cmd.unused, cmd.unused, cmd.unused]))
    callback(trueRet)

    return self
  },

  /** Rotate right (both motor moving in the opposite direction) **/
  right_with_rotation: function(callback, opts) {
    if (typeof opts == 'undefined')
      opts = {}

    self.write_i2c_block(cmd.right_rot.concat([cmd.unused, cmd.unused, cmd.unused]))
    callback(trueRet)

    return self
  },

  /** Stop **/
  stop: function(callback) {
    self.write_i2c_block(cmd.stop.concat([cmd.unused, cmd.unused, cmd.unused]))
    callback(trueRet)

    return self
  },

  /** Increase speed **/
  increase_speed: function(callback) {
    self.write_i2c_block(cmd.ispd.concat([cmd.unused, cmd.unused, cmd.unused]))
    callback(trueRet)

    return self
  },

  /** Decrease speed **/
  decrease_speed: function(callback) {
    self.write_i2c_block(cmd.dspd.concat([cmd.unused, cmd.unused, cmd.unused]))
    callback(trueRet)

    return self
  },

  /** Trim test with the value specified */
  trim_test: function(value, callback) {
    if (value > 100) {
      value = 100
    } else if (value < -100) {
      vaue = -100
    }
    value += 100

    self.write_i2c_block(cmd.trim_test.concat([value, cmd.unused, cmd.unused]))
    callback(trueRet)

    return self
  },

  /** Read the trim value in EEPROM if present else return -3 **/
  trim_read: function(callback) {
    self.write_i2c_block(cmd.trim_read.concat([cmd.unused, cmd.unused, cmd.unused]))
    self.utils.wait(80)

    var b1 = self.read_i2c_byte()
    var b2 = self.read_i2c_byte()

    if (b1 != -1 && b2 != -1) {
      var value = b1 * 256 + b2
      if (value == 255) {
        callback(-3)
      } else {
        callback(value)
      }
    } else {
      callback(falseRet)
    }

    return self
  },

  /** Write the trim value to EEPROM, where -100=0 and 100=200 */
  trim_write: function(value, callback) {
    if (value > 100) {
      value = 100
    } else if (value < -100) {
      vaue = -100
    }
    value += 100

    self.write_i2c_block(cmd.trim_write.concat([value, cmd.unused, cmd.unused]))
    callback(trueRet)

    return self
  },

  /** Read voltage (Returns voltage in V) **/
  volt: function(callback) {
    self.write_i2c_block(cmd.volt.concat([cmd.unused, cmd.unused, cmd.unused]))
    self.utils.wait(100)

    var b1 = self.read_i2c_byte()
    var b2 = self.read_i2c_byte()

    if (b1 != -1 && b2 != -1) {
      var value = b1 * 256 + b2
      value = +(Number(parseFloat((5 * value / 1024) / .4))).toFixed(2)
      callback(value)
    } else {
      callback(falseRet)
    }

    return self
  },

  /** Read ultrasonic sensor (returns distance in centimeters) **/
  ultrasonic_distance: function(pin, callback) {
    self.write_i2c_block(cmd.us.concat([pin, cmd.unused, cmd.unused]))
    self.utils.wait(80)

    var b1 = self.read_i2c_byte()
    var b2 = self.read_i2c_byte()

    if (b1 != -1 && b2 != -1) {
      var value = b1 * 256 + b2
      callback(value)
    } else {
      callback(falseRet)
    }

    return self
  },

  /** Turn led on **/
  led_on: function(ledID, callback) {
    if (ledID == self.LED_L_PIN || ledID == self.LED_R_PIN) {
      self.digitalWrite(ledID, 1)
      callback(trueRet)
    } else {
      callback(falseRet)
    }

    return self
  },

  /** Turn led off **/
  led_off: function(ledID, callback) {
    if (ledID == self.LED_L_PIN || ledID == self.LED_R_PIN) {
      self.digitalWrite(ledID, 0)
      callback(trueRet)
    } else {
      callback(falseRet)
    }

    return self
  },

  /** Set servo position (position is expressed in angle degrees) **/
  servo: function(position, callback) {
    self.write_i2c_block(cmd.servo.concat([position, cmd.unused, cmd.unused]))
    callback(trueRet)

    return self
  },

  /** Set encoder targeting on **/
  /** m1: 0 to disable targeting for m1, 1 to enable it **/
  /** m2: 1 to disable targeting for m2, 1 to enable it **/
  /** target: number of encoder pulses to target (18 per revolution) **/
  encoder_targeting: function(m1, m2, target, callback) {
    if (m1 > 1 || m1 < 0 || m2 > 1 || m2 < 0) {
      callback(falseRet)
    } else {
      var m_sel = m1 * 2 + m2
      self.write_i2c_block(cmd.enc_tgt.concat([m_sel, target / 256, target % 256]))
      callback(trueRet)
    }

    return self
  },

  /** Read encoder value **/
  /** motor: 0 for motor1 and 1 for motor2 **/
  /** return distance in cm **/
  encoder_read: function(motor) {
    self.write_i2c_block(cmd.enc_read.concat([motor, cmd.unused, cmd.unused]))
    self.utils.wait(80)

    var b1 = self.read_i2c_byte()
    var b2 = self.read_i2c_byte()

    if (b1 != -1 && b2 != -1) {
      var value = b1 * 256 + b2
      callback(value)
    } else {
      callback(falseRet)
    }

    return self
  },

  /** Firmware version **/
  version: function(callback) {
    self.write_i2c_block(cmd.fw_ver.concat([cmd.unused, cmd.unused, cmd.unused]))
    self.utils.wait(100)
    var value = self.read_i2c_byte()
    self.read_i2c_byte() // Empty the buffer
    if (value == falseRet) {
      callback(falseRet)
    } else {
      value /= 10
      callback(value)
    }

    return self
  },

  /** Enable the encoders (enabled by default) **/
  enable_encoders: function(callback) {
    self.write_i2c_block(cmd.en_enc.concat([cmd.unused, cmd.unused, cmd.unused]))
    callback(trueRet)

    return self
  },

  /** Disable the encoders (use this if you don't want to use the encoders) **/
  disable_encoders: function(callback) {
    self.write_i2c_block(cmd.dis_enc.concat([cmd.unused, cmd.unused, cmd.unused]))
    callback(trueRet)

    return self
  },

  /** Enable the servo **/
  enable_servo: function(callback) {
    self.write_i2c_block(cmd.en_servo.concat([cmd.unused, cmd.unused, cmd.unused]))
    callback(trueRet)

    return self
  },

  /** Disable the servo **/
  disable_servo: function(callback) {
    self.write_i2c_block(cmd.dis_servo.concat([cmd.unused, cmd.unused, cmd.unused]))
    callback(trueRet)

    return self
  },

  /** Set speed of the left motor **/
  /** speed => 0-255 **/
  set_left_speed: function(speed, callback) {
    if (speed > 255) speed = 255
    else if (speed < 0) speed = 0

    self.write_i2c_block(cmd.set_left_speed.concat([speed, cmd.unused, cmd.unused]))
    callback(trueRet)

    return self
  },

  /** Set speed of the right motor **/
  /** speed => 0-255 **/
  set_right_speed: function(speed, callback) {
    if (speed > 255) speed = 255
    else if (speed < 0) speed = 0

    self.write_i2c_block(cmd.set_right_speed.concat([speed, cmd.unused, cmd.unused]))
    callback(trueRet)

    return self
  },

  /** Set speed of the both motors **/
  /** speed => 0-255 **/
  set_speed: function(speed, callback) {
    if (speed > 255) speed = 255
    else if (speed < 0) speed = 0

    self.write_i2c_block(cmd.set_left_speed.concat([speed, cmd.unused, cmd.unused]))
    self.utils.wait(100)
    self.write_i2c_block(cmd.set_right_speed.concat([speed, cmd.unused, cmd.unused]))
    callback(trueRet)

    return self
  },

  /** Enable communication time-out (stop the motors if no command received in the specified time-out) **/
  /** timeout => 0-65535 **/
  enable_communication_timeout: function(timeout) {
    self.write_i2c_block(cmd.en_com_timeout.concat([timeout / 256, timeout % 256, cmd.unused]))
    callback(trueRet)

    return self
  },

  /** Disable communication time-out **/
  disable_communication_timeout: function(timeout) {
    self.write_i2c_block(cmd.dis_com_timeout.concat([cmd.unused, cmd.unused, cmd.unused]))
    callback(trueRet)

    return self
  },

  /** Read the status register on the GoPiGo **/
  /**
    Gets a byte,  b0-enc_status
        b1-timeout_status
    Return: list with   l[0]-enc_status
        l[1]-timeout_status
  **/
  read_status: function(callback) {
    var status = self.read_i2c_byte()
    var register = [status & (1 << 0), (status & (1 << 1))/2]
    callback(register)

    return self
  },

  /** Read encoder status **/
  /** return 0 if encoder target is reached **/
  read_encoder_status: function(callback) {
    self.read_status(function onStatus(res) {
      callback(res[0])
    })

    return self
  },

  /** Read timeout status **/
  read_timeout_status: function(callback) {
    self.read_status(function onStatus(res) {
      callback(res[1])
    })

    return self
  },

  /*
   *
   * Utils functions
   *
   */
  utils: {
    debug: function(msg) {
      if (debug)
        log.info('', msg)
    },
    wait: function(ms) {
      sleep.usleep(1000 * ms)
    },
    checkVoltage: function(callback) {
      self.utils.debug('voltage check')

      self.volt(function onVoltage(res) {
        if (res > 0 && res <= minVoltage) {
          self.utils.debug('voltage ('+res+') is under the minimum value')
          callback(res)
        }
      })
    }
  }
}
