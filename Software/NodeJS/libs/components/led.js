var commands   = require('../commands')

Led.LEFT_PIN = 10
Led.RIGHT_PIN = 5
Led.LEFT = 1
Led.RIGHT = 0

function Led(gopigo, id) {
  this.gopigo = gopigo
  this.pin = id == Led.LEFT ? Led.LEFT_PIN : Led.RIGHT_PIN
}

Led.prototype = new Led()

Led.prototype.on = function() {
  return this.gopigo.board.digitalWrite(this.pin, 1)
}
Led.prototype.off = function() {
  return this.gopigo.board.digitalWrite(this.pin, 0)
}

module.exports = Led