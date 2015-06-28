var commands   = require('../commands')

Led.LEFT_PIN_A = 10
Led.LEFT_PIN_B = 17
Led.RIGHT_PIN_A = 5
Led.RIGHT_PIN_B = 16
Led.LEFT = 1
Led.RIGHT = 0

var self

function Led(gopigo, id) {
  self = this
  this.gopigo = gopigo
  this.pin = 0
  this.id = id
}

Led.prototype.setPin = function() {
  var vol = this.gopigo.board.analogRead(7)
  var left_pin = 0
  var right_pin = 0
  if (vol > 700) {
    left_pin = Led.LEFT_PIN_B
    right_pin = Led.RIGHT_PIN_B
  } else {
    left_pin = Led.LEFT_PIN_A
    right_pin = Led.RIGHT_PIN_A
  }
  this.pin = this.id == Led.LEFT ? left_pin : right_pin
}
Led.prototype.on = function() {
  if (this.pin == 0) {
    this.setPin()
  }
  this.gopigo.board.pinMode(this.pin, this.gopigo.board.OUTPUT)
  return this.gopigo.board.digitalWrite(this.pin, 1)
}
Led.prototype.off = function() {
  if (this.pin == 0) {
    this.setPin()
  }
  this.gopigo.board.pinMode(this.pin, this.gopigo.board.OUTPUT)
  return this.gopigo.board.digitalWrite(this.pin, 0)
}

module.exports = Led