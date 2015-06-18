var commands   = require('../commands')

var self

function Encoders(gopigo) {
  self = this
  this.gopigo = gopigo
}

Encoders.prototype.targeting = function(m1, m2, target) {
  if (m1 > 1 || m1 < 0 || m2 > 1 || m2 < 0)
    return false
  var mSel = m1 * 2 + m2
  return this.gopigo.board.writeBytes(commands.enc_tgt.concat([mSel, target / 256, target % 256]))
}
Encoders.prototype.read = function(motor) {
  var write = this.gopigo.board.writeBytes(commands.enc_read.concat([motor, commands.unused, commands.unused]))
  if (write) {
    this.gopigo.board.wait(80)
    var b1 = this.gopigo.board.readByte()
    var b2 = this.gopigo.board.readByte()
    if (b1[0] != -1 && b2[0] != -1) {
      return b1[0] * 256 + b2[0]
    } else
      return false
  } else {
    return false
  }
}
Encoders.prototype.readStatus = function() {
  var status = this.gopigo.board.readStatus()
  return status[0]
}
Encoders.prototype.enable = function() {
  return this.gopigo.board.writeBytes(commands.en_enc.concat([commands.unused, commands.unused, commands.unused]))
}
Encoders.prototype.disable = function() {
  return this.gopigo.board.writeBytes(commands.dis_enc.concat([commands.unused, commands.unused, commands.unused]))
}

module.exports = Encoders
