var commands   = require('../commands')

Motion.directions = {
  'n' : 0,
  'ne': 45,
  'e' : 90,
  'se': 135,
  's' : 180,
  'sw': 225,
  'w' : 270,
  'nw': 315
}

var self

function Motion(gopigo) {
  self = this
  this.gopigo = gopigo
}

Motion.prototype.forward = function(usePid) {
  var command = usePid ? commands.fwd : commands.motor_fwd
  return this.gopigo.board.writeBytes(command.concat([commands.unused, commands.unused, commands.unused]))
}
Motion.prototype.backward = function(usePid) {
  var command = usePid ? commands.bwd : commands.motor_bwd
  return this.gopigo.board.writeBytes(command.concat([commands.unused, commands.unused, commands.unused]))
}
Motion.prototype.left = function() {
  return this.gopigo.board.writeBytes(commands.left.concat([commands.unused, commands.unused, commands.unused]))
}
Motion.prototype.leftWithRotation = function() {
  return this.gopigo.board.writeBytes(commands.left_rot.concat([commands.unused, commands.unused, commands.unused]))
}
Motion.prototype.right = function() {
  return this.gopigo.board.writeBytes(commands.right.concat([commands.unused, commands.unused, commands.unused]))
}
Motion.prototype.rightWithRotation = function() {
  return this.gopigo.board.writeBytes(commands.right_rot.concat([commands.unused, commands.unused, commands.unused]))
}
Motion.prototype.stop = function() {
  return this.gopigo.board.writeBytes(commands.stop.concat([commands.unused, commands.unused, commands.unused]))
}
Motion.prototype.increaseSpeed = function() {
  return this.gopigo.board.writeBytes(commands.ispd.concat([commands.unused, commands.unused, commands.unused]))
}
Motion.prototype.decreaseSpeed = function() {
  return this.gopigo.board.writeBytes(commands.dspd.concat([commands.unused, commands.unused, commands.unused]))
}
Motion.prototype.setLeftSpeed = function(speed) {
  if (speed > 255)
    speed = 255
  else if (speed < 0)
    speed = 0

  return this.gopigo.board.writeBytes(commands.set_left_speed.concat([speed, commands.unused, commands.unused]))
}
Motion.prototype.setRightSpeed = function(speed) {
  if (speed > 255)
    speed = 255
  else if (speed < 0)
    speed = 0

  return this.gopigo.board.writeBytes(commands.set_right_speed.concat([speed, commands.unused, commands.unused]))
}
Motion.prototype.setSpeed = function(speed) {
  this.setLeftSpeed(speed)
  this.setRightSpeed(speed)
}
Motion.prototype.trimTest = function(value) {
  if (value > 100)
    value = 100
  else if (value < -100)
    value = -100
  value += 100

  return this.gopigo.board.writeBytes(commands.trim_test.concat([value, commands.unused, commands.unused]))
}
Motion.prototype.trimRead = function() {
  var write = this.gopigo.board.writeBytes(commands.trim_read.concat([this.pin, commands.unused, commands.unused]))
  if (write) {
    this.gopigo.board.wait(80)
    var b1 = this.gopigo.board.readByte()
    var b2 = this.gopigo.board.readByte()
    if (b1[0] != -1 && b2[0] != -1) {
      var val = b1[0] * 256 + b2[0]
      if (val == 255)
        return -3
      return val
    } else
      return false
  } else {
    return false
  }
}
Motion.prototype.trimWrite = function(value) {
  if (value > 100)
    value = 100
  else if (value < -100)
    value = -100
  value += 100

  return this.gopigo.board.writeBytes(commands.trim_write.concat([value, commands.unused, commands.unused]))
}
Motion.prototype.readTimeoutStatus = function() {
  var status = this.gopigo.board.readStatus()
  return status[1]
}
Motion.prototype.enableCommunicationTimeout = function(timeout) {
  return this.gopigo.board.writeBytes(commands.en_com_timeout.concat([timeout, commands.unused, commands.unused]))
}
Motion.prototype.disableCommunicationTimeout = function() {
  return this.gopigo.board.writeBytes(commands.dis_com_timeout.concat([commands.unused, commands.unused, commands.unused]))
}

module.exports = Motion