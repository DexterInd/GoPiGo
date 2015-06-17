var commands   = require('../commands')

Led.LEFT_PIN_A = 10
Led.RIGHT_PIN_A = 5
Led.LEFT_PIN_B = 17
Led.RIGHT_PIN_B = 16
Led.LEFT = 1
Led.RIGHT = 0

function Led(gopigo, id) {
  this.gopigo = gopigo
  var vol = this.gopigo.analogRead(7)
  var left_pin = 0
  var right_pin = 0
  if (vol > 700) {
    left_pin = Led.LEFT_PIN_B
    right_pin = Led.RIGHT_PIN_B
  } else {
    left_pin = Led.LEFT_PIN_A
    right_pin = Led.RIGHT_PIN_A
  }
  this.pin = id == Led.LEFT ? left_pin : right_pin
}

Led.prototype = new Led()

Led.prototype.on = function() {
  this.gopigo.pinMode(this.pin, this.gopigo.OUTPUT)
  return this.gopigo.board.digitalWrite(this.pin, 1)
}
Led.prototype.off = function() {
  this.gopigo.pinMode(this.pin, this.gopigo.OUTPUT)
  return this.gopigo.board.digitalWrite(this.pin, 0)
}

module.exports = Led