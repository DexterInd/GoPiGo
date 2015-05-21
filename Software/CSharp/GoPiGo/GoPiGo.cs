using System;
using Windows.Devices.I2c;

namespace GoPiGo
{
    public interface IGoPiGo
    {
        string GetFirmwareVersion();
        byte DigitalRead(Pin pin);
        void DigitalWrite(Pin pin, byte value);
        int AnalogRead(Pin pin);
        void AnalogWrite(Pin pin, byte value);
        void PinMode(Pin pin, PinMode mode);
        decimal BatteryVoltage();
        IMotorController MotorController();
        //Currently not functioning
        //IEncoderController EncoderController();
        IGoPiGo RunCommand(Commands command, byte firstParam = Constants.Unused, byte secondParam = Constants.Unused, byte thirdParam = Constants.Unused);
    }

    public class GoPiGo : IGoPiGo
    {
        private readonly IMotorController _motorController;
        private readonly IEncoderController _encoderController;

        internal GoPiGo(I2cDevice device)
        {
            if (device == null) throw new ArgumentNullException(nameof(device));
            DirectAccess = device;
            _motorController = new MotorController(this);
            _encoderController = new EncoderController(this);
        }

        public IMotorController MotorController()
        {
            return _motorController;
        }

        public IEncoderController EncoderController()
        {
            return _encoderController;
        }

        internal I2cDevice DirectAccess { get; }

        public string GetFirmwareVersion()
        {
            var buffer = new[] { (byte)Commands.Version, Constants.Unused, Constants.Unused, Constants.Unused };
            DirectAccess.Write(buffer);
            DirectAccess.Read(buffer);
            return $"{buffer[0]}";
        }

        public byte DigitalRead(Pin pin)
        {
            var buffer = new[] { (byte)Commands.DigitalRead, (byte)pin, Constants.Unused, Constants.Unused };
            DirectAccess.Write(buffer);

            var readBuffer = new byte[1];
            DirectAccess.Read(readBuffer);
            return readBuffer[0];
        }

        public void DigitalWrite(Pin pin, byte value)
        {
            var buffer = new[] { (byte)Commands.DigitalWrite, (byte)pin, value, Constants.Unused };
            DirectAccess.Write(buffer);
        }

        public int AnalogRead(Pin pin)
        {
            var buffer = new[]
            {(byte) Commands.DigitalRead, (byte) Commands.AnalogRead, (byte) pin, Constants.Unused, Constants.Unused};
            DirectAccess.Write(buffer);
            DirectAccess.Read(buffer);
            return buffer[1] * 256 + buffer[2];
        }

        public void AnalogWrite(Pin pin, byte value)
        {
            var buffer = new[] { (byte)Commands.AnalogWrite, (byte)pin, value, Constants.Unused };
            DirectAccess.Write(buffer);
        }

        public void PinMode(Pin pin, PinMode mode)
        {
            var buffer = new[] { (byte)Commands.PinMode, (byte)pin, (byte)mode, Constants.Unused };
            DirectAccess.Write(buffer);
        }


        public decimal BatteryVoltage()
        {
            var buffer = new[] { (byte)Commands.BatteryVoltage, Constants.Unused, Constants.Unused, Constants.Unused };

            DirectAccess.Write(buffer);
            DirectAccess.Read(buffer);

            decimal voltage = buffer[1] * 256 + buffer[2];
            voltage = (5 * voltage / 1024) / (decimal).4;

            return Math.Round(voltage, 2);
        }

        public IGoPiGo RunCommand(Commands command, byte firstParam = Constants.Unused, byte secondParam = Constants.Unused, byte thirdParam = Constants.Unused)
        {
            var buffer = new[] { (byte)command, firstParam, secondParam, thirdParam };
            DirectAccess.Write(buffer);
            return this;
        }
    }
}
