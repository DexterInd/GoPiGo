var util         = require('util')
var EventEmitter = require('events').EventEmitter
var log          = require('npmlog')
var sleep        = require('sleep')

var Board        = require('./components/board')
var Encoders     = require('./components/encoders')
var Led          = require('./components/led')
var Motor        = require('./components/motor')
var Servo        = require('./components/servo')
var UltraSonicSensor = require('./components/ultraSonicSensor')
var IRReceiverSensor = require('./components/IRReceiverSensor')
var Motion       = require('./behaviours/motion')

var initWait  = 1     // in seconds

var isInit    = false
var isHalt    = false
var isBusy    = false

var ADDRESS   = 0x08

var voltageInterval      = null
var voltageIntervalDelay = 60000    // in milliseconds (1 min.)
var minVoltage           = 5.5      // in Volts
var criticalVoltage      = 1.0      // in Volts

var debugMode = false

var self

function GoPiGo(opts) {
  self = this

  if (typeof opts == 'undefined')
    opts = {}

  if (typeof opts.minVoltage != 'undefined')
    this.minVoltage = opts.minVoltage
  else
    this.minVoltage = minVoltage

  if (typeof opts.criticalVoltage != 'undefined')
    this.criticalVoltage = opts.criticalVoltage
  else
    this.criticalVoltage = criticalVoltage

  if (typeof opts.debug != 'undefined')
    this.debugMode = opts.debug
  else
    this.debugMode = debugMode

  try {
    this.board            = new Board(this)
    this.encoders         = new Encoders(this)
    this.servo            = new Servo(this)
    if (typeof opts.ultrasonicSensorPin != 'undefined')
      this.ultraSonicSensor = new UltraSonicSensor(this, opts.ultrasonicSensorPin)
    if (typeof opts.IRReceiverSensorPin != 'undefined')
      this.IRReceiverSensor = new IRReceiverSensor(this, opts.IRReceiverSensorPin)
    this.ledLeft          = new Led(this, Led.LEFT)
    this.ledRight         = new Led(this, Led.RIGHT)
    this.motorLeft        = new Motor(this, Motor.LEFT)
    this.motorRight       = new Motor(this, Motor.RIGHT)
    this.motion           = new Motion(this)
  } catch (err) {
    this.emit('error', err)
  }
}

util.inherits(GoPiGo, EventEmitter)

GoPiGo.prototype.init = function() {
  if (!isHalt) {
    if (!isInit) {
      this.board.init()

      this.debug('GoPiGo is initing')
      sleep.sleep(initWait)
      isInit = true

      this.debug('GoPiGo will check the voltage each ' + voltageIntervalDelay + ' milliseconds')
      voltageInterval = setInterval(this.checkVoltage, voltageIntervalDelay)
      this.checkVoltage()
      this.reset()

      this.emit('init', true)
    } else {
      var err = new Error('GoPiGo is already initialized')
      this.emit('init', false)
      this.emit('error', err)
    }
  } else {
    var err = new Error('GoPiGo cannot be initialized')
    this.emit('init', false)
    this.emit('error', err)
  }
}
GoPiGo.prototype.checkVoltage = function() {
  self.debug('Voltage check')

  var voltage = self.board.getVoltage()
  if (voltage > 0 && voltage <= self.minVoltage) {
    self.debug('Voltage ('+voltage+') is under the minimum value')
    self.free()
    self.emit('lowVoltage', voltage)
  } else if (voltage > self.minVoltage && voltage <= self.criticalVoltage) {
    self.debug('Voltage ('+voltage+') is under the critical value')
    self.halt()
    self.emit('criticalVoltage', voltage)
  } else {
    self.free()
    self.emit('normalVoltage', voltage)
  }
}
GoPiGo.prototype.free = function() {
  if (isHalt) {
    this.debug('The GoPiGo is changing status from HALT to FREE')
    isHalt = false
    this.emit('free', !isHalt)
  }
}
GoPiGo.prototype.halt = function() {
  if (!isHalt) {
    this.debug('The GoPiGo is changing status from FREE to HALT')
    isHalt = true
    this.emit('halt', isHalt)
  }
}
GoPiGo.prototype.close = function() {
  this.board.close
  this.emit('close', true)
}
GoPiGo.prototype.isOperative = function() {
  return isHalt == false
}
GoPiGo.prototype.isHalt = function() {
  return isHalt
}
GoPiGo.prototype.checkStatus = function() {
  if (!isInit || isHalt){
    if (!isHalt) {
      this.debug('GoPiGo needs to be initialized.')
    } else {
      this.debug('GoPiGo is not operative because halted')
    }
    return false
  }
  return true
}
GoPiGo.prototype.reset = function() {
  this.debug('GoPiGo is resetting')
  this.servo.move(Motion.directions.e)
  this.ledRight.off()
  this.ledLeft.off()
  this.motion.setSpeed(255)
  this.free()
  this.emit('reset', true)
}
GoPiGo.prototype.debug = function(msg) {
  if (this.debugMode)
    log.info('GoPiGo.board', msg)
}

module.exports = GoPiGo
