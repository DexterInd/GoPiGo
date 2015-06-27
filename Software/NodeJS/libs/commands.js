module.exports = {
    fwd                                         : [119]   // Move forward with PID
  , motor_fwd                                   : [105]   // Move forward without PID
  , bwd                                         : [115]   // Move back with PID
  , motor_bwd                                   : [107]   // Move back without PID
  , left                                        : [97]    // Turn Left by turning off one motor
  , left_rot                                    : [98]    // Rotate left by running both motors is opposite direction
  , right                                       : [100]   // Turn Right by turning off one motor
  , right_rot                                   : [110]   // Rotate Right by running both motors is opposite direction
  , stop                                        : [120]   // Stop the GoPiGo
  , ispd                                        : [116]   // Increase the speed by 10
  , dspd                                        : [103]   // Decrease the speed by 10
  , m1                                          : [111]   // Control motor1
  , m2                                          : [112]   // Control motor2

  , volt                                        : [118]   // Read the voltage of the batteries
  , us                                          : [117]   // Read the distance from the ultrasonic sensor
  , led                                         : [108]   // Turn On/Off the LED's
  , servo                                       : [101]   // Rotate the servo
  , enc_tgt                                     : [50]    // Set the encoder targeting
  , fw_ver                                      : [20]    // Read the firmware version
  , en_enc                                      : [51]    // Enable the encoders
  , dis_enc                                     : [52]    // Disable the encoders
  , read_enc_status                             : [53]    // Read encoder status
  , en_servo                                    : [61]    // Enable the servo's
  , dis_servo                                   : [60]    // Disable the servo's
  , set_left_speed                              : [70]    // Set the speed of the right motor
  , set_right_speed                             : [71]    // Set the speed of the left motor
  , en_com_timeout                              : [80]    // Enable communication timeout
  , dis_com_timeout                             : [81]    // Disable communication timeout
  , timeout_status                              : [82]    // Read the timeout status
  , enc_read                                    : [53]    // Read encoder values
  , trim_test                                   : [30]    // Test the trim values
  , trim_write                                  : [31]    // Write the trim values
  , trim_read                                   : [32]

  , dWrite                                      : [12]    // Digital write on a port
  , dRead                                       : [13]    // Digital read on a port
  , aRead                                       : [14]    // Analog read on a port
  , aWrite                                      : [15]    // Analog read on a port
  , pMode                                       : [16]    // Set up the pin mode on a port

  // Grove IR sensor
  // Read the button from IR sensor
  , irRead                                      : [21]
  // Set pin for the IR reciever
  , irRecvPin                                   : [22]

  // This allows us to be more specific about which commands contain unused bytes
  , unused                                      : 0
};
