var commands   = require('../commands')

var self

function UltraSonicSensor(gopigo, pin) {
  self = this
  this.gopigo = gopigo
  this.pin = pin
}

UltraSonicSensor.prototype.setPin = function(pin) {
  this.pin = pin
}
UltraSonicSensor.prototype.getDistance = function() {
  var write = this.gopigo.board.writeBytes(commands.us.concat([this.pin, commands.unused, commands.unused]))
  if (write) {
    this.gopigo.board.wait(80)
    var b1 = this.gopigo.board.readByte()
    var b2 = this.gopigo.board.readByte()
    if (b1[0] != -1 && b2[0] != -1)
      return (b1[0] * 256 + b2[0])
    else
      return false
  } else {
    return false
  }
}

module.exports = UltraSonicSensor