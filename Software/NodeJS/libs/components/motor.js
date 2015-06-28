var commands   = require('../commands')

Motor.LEFT_COMMAND = 10
Motor.RIGHT_COMMAND = 5
Motor.FORWARD = 1
Motor.BACKWARD = 0
Motor.LEFT = 1
Motor.RIGHT = 0

var self

function Motor(gopigo, id) {
  self = this
  this.gopigo = gopigo
  this.command = id == Motor.LEFT ? Motor.LEFT_COMMAND : Motor.RIGHT_COMMAND
}

Motor.prototype.move = function(direction, speed) {
  return this.gopigo.board.writeBytes(this.command.concat([direction, speed, commands.unused]))
}

module.exports = Motor