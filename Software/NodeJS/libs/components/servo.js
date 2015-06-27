var commands   = require('../commands')

var self

function Servo(gopigo) {
  self = this
  this.gopigo = gopigo
}

Servo.prototype.move = function(position) {
  var write = this.gopigo.board.writeBytes(commands.servo.concat([position, commands.unused, commands.unused]))
  if (write) {
    this.position = position
    return true
  } else {
    return false
  }
}
Servo.prototype.enable = function() {
  return this.gopigo.board.writeBytes(commands.en_servo.concat([commands.unused, commands.unused, commands.unused]))
}
Servo.prototype.disable = function() {
  return this.gopigo.board.writeBytes(commands.dis_servo.concat([commands.unused, commands.unused, commands.unused]))
}

module.exports = Servo