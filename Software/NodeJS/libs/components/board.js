var util         = require('util')
var EventEmitter = require('events').EventEmitter

var commands    = require('../commands')

var i2c         = require('i2c-bus')
var log         = require('npmlog')
var sleep       = require('sleep')
var fs          = require('fs')
var bufferTools = require('buffertools').extend()

var I2CCMD    = 1
var debugMode = false
var i2c0Path  = '/dev/i2c-0'
var i2c1Path  = '/dev/i2c-1'
var bus
var busNumber

var ADDRESS   = 0x08

var self

function Board(gopigo) {
  self = this
  this.gopigo = gopigo

  this.BYTESLEN = 4
  this.INPUT = 'input'
  this.OUTPUT = 'output'

  if (fs.existsSync(i2c0Path)) {
    busNumber = 0
  } else if (fs.existsSync(i2c1Path)) {
    busNumber = 1
  } else {
    this.gopigo.halt()
  }
}

util.inherits(Board, EventEmitter)

Board.prototype.init = function() {
  try {
    bus = i2c.openSync(busNumber)
  } catch (err) {
    this.gopigo.halt()
  }
}
Board.prototype.close = function() {
  if (typeof bus != 'undefined') {
    this.gopigo.debug('GoPiGo is closing')
    bus.closeSync()
  } else {
    this.gopigo.debug('The device is not defined')
  }
}
Board.prototype.readByte = function() {
  var isOperative = this.gopigo.checkStatus()
  if (!isOperative)
    return false

  var length = 1
  var buffer = new Buffer(length)
  var ret = bus.i2cReadSync(ADDRESS, length, buffer)
  return ret > 0 ? buffer : false
}
Board.prototype.readBytes = function(length) {
  if (typeof length == 'undefined')
    length = this.BYTESLEN

  var isOperative = this.gopigo.checkStatus()
  if (!isOperative)
    return false

  var buffer = new Buffer(length)
  var ret = false
  try {
    var val = bus.i2cReadSync(ADDRESS, length, buffer)
    ret = val > 0 ? buffer : false
  } catch (err) {
    ret = false
  } finally {
    return ret
  }
}
Board.prototype.writeBytes = function(bytes) {
  var isOperative = this.gopigo.checkStatus()
  if (!isOperative)
    return false

  var buffer = new Buffer(bytes)
  var ret = false
  try {
    this.wait(100)  // TODO: is this needed?
    var val = bus.i2cWriteSync(ADDRESS, buffer.length, buffer)
    ret = val > 0 ? true : false
  } catch (err) {
    ret = false
  } finally {
    return ret
  }
}
Board.prototype.analogRead = function(pin, length) {
  /*
  if (pin != 1)
    return false
  */

  if (typeof length == 'undefined')
    length = this.BYTESLEN

  var writeRet = this.writeBytes(commands.aRead.concat([pin, commands.unused, commands.unused]))
  if (writeRet) {
    this.wait(50)
    var b1 = this.readByte()
    var b2 = this.readByte()
    if (b1[0] != -1 && b2[0] != -1) {
      return b1[0] * 256 + b2[0]
    } else {
      return false
    }
  } else {
    return false
  }
}
Board.prototype.analogWrite = function(pin, value) {
  if (pin != 10)
    return false

  var write = this.writeBytes(commands.aWrite.concat([pin, value, commands.unused]))
  this.wait(5)
  return true
}
Board.prototype.digitalRead = function(pin) {
  var writeRet = this.writeBytes(commands.dRead.concat([pin, commands.unused, commands.unused]))
  if (writeRet) {
    return this.readByte()[0]
  } else {
    return false
  }
}
Board.prototype.digitalWrite = function(pin, value) {
  // if (pin == 10 || pin == 0 || pin == 1 || pin == 5 || pin == 16 || pin == 17)
  if (value == 0 || value == 1)
    return this.writeBytes(commands.dWrite.concat([pin, value, commands.unused]))
  else
    return false
}
Board.prototype.pinMode = function(pin, mode) {
  var isOperative = this.gopigo.checkStatus()
  if (!isOperative)
    return false
  // if (pin == 10 || pin == 15 || pin == 0 || pin == 1)
  if (mode == this.OUTPUT) {
    return this.writeBytes(commands.pMode.concat([pin, 1, commands.unused]))
  } else if (mode == this.INPUT) {
    return this.writeBytes(commands.pMode.concat([pin, 0, commands.unused]))
  } else {
    this.gopigo.debug('Unknown pin mode, given mode was ' + mode)
  }
}
Board.prototype.wait = function(ms) {
  sleep.usleep(1000 * ms)
}
Board.prototype.getVoltage = function() {
  var write = this.writeBytes(commands.volt.concat([commands.unused, commands.unused, commands.unused]))
  if (write) {
    this.wait(100)
    var b1 = this.readByte()
    var b2 = this.readByte()
    if (b1[0] != -1 && b2[0] != -1) {
      var voltage = b1[0] * 256 + b2[0]
      voltage = (5 * voltage / 1024) / .4
      voltage = Math.round(voltage * 100.0) / 100.0
      return voltage
    } else
      return false
  } else {
    return false
  }
}
Board.prototype.version = function() {
  var write = this.writeBytes(commands.fw_ver.concat([commands.unused, commands.unused, commands.unused]))
  if (write) {
    this.wait(100)
    var byte = this.readByte()
    this.readByte()
    if (byte instanceof Buffer) {
      var version = byte[0] / 10
      return version
    } else
      return false
  } else {
    return false
  }
}
Board.prototype.revision = function() {
  var write = this.writeBytes(commands.aRead.concat([7, commands.unused, commands.unused]))
  if (write) {
    this.wait(100)
    var b1 = this.readByte()
    var b2 = this.readByte()
    if (b1[0] != -1 && b2[0] != -1) {
      return b1[0] * 256 + b2[0]
    } else {
      return false
    }
  } else {
    return false
  }
}
Board.prototype.readStatus = function() {
  var byte = this.readByte()
  if (byte instanceof Buffer) {
    var statusReg = []
    statusReg[0] = byte[0] & (1 << 0)
    statusReg[1] = (byte[0] & (1 << 1)) / 2
    return statusReg
  } else
    return false
}

module.exports = Board
