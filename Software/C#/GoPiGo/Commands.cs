namespace GoPiGo
{
    public enum Commands
    {
        Version = 20,
        BatteryVoltage = 118,
        UltraSonic = 117,

        DigitalWrite = 12,
        DigitalRead = 13,
        AnalogRead = 14,
        AnalogWrite = 15,
        PinMode = 16,
        MoveForward = 119,
        MoveForwardNoPid = 105,
        MoveBackward = 115,
        MoveBackwardNoPid = 107,
        MoveLeft = 97,
        RotateLeft = 98,
        MoveRight = 100,
        RotateRight = 110,
        Stop = 120,
        IncreaseSpeedBy10 = 116,
        DecreaseSpeedBy10 = 103,
        MotorOne = 111,
        MotorTwo = 112,
        SetLeftMotorSpeed = 70,
        SetRightMotorSpeed = 71,

        RotateServo = 101,
        EnableServo = 61,
        DisableServo = 60,

        SetEncoderTargeting = 50,
        EnableEncoder = 51,
        DisableEncoder = 52,
        ReadEncoder = 53,

        EnableCommunicationTimeout = 80,
        DisableCommunicationTimeout = 81,
        ReadTimeoutStatus = 82,

        TrimTest = 30,
        WriteTrim = 31,
        ReadTrim = 32
    }
}
