var commands   = require('../commands')

var self

function IRReceiverSensor(gopigo, pin) {
  self = this
  this.gopigo = gopigo
  this.pin = pin
}

IRReceiverSensor.prototype.setPin = function(pin) {
  this.pin = pin + 1
}
IRReceiverSensor.prototype.read = function() {
  this.write(commands.unused)
  var write = this.gopigo.board.writeBytes(commands.irRead.concat([commands.unused, commands.unused, commands.unused]))
  if (write) {
    this.gopigo.board.wait(100)
    this.board.readByte()
    var bytes = this.board.readBytes(22)
    if (bytes instanceof Buffer && bytes[1] != 255) {
      bytes.slice(0,1)
      return bytes
    } else {
      return false
    }
  } else {
    return false
  }
}
IRReceiverSensor.prototype.write = function(value) {
  return this.gopigo.board.writeBytes(commands.irRecvPin.concat([this.pin, value, commands.unused]))
}

module.exports = IRReceiverSensor