using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GoPiGo.Sensors
{
    public abstract class Sensor<TSensorType> where TSensorType : class
    {
        protected readonly IGoPiGo Device;
        protected readonly Pin Pin;

        internal Sensor(IGoPiGo device, Pin pin, PinMode pinMode)
        {
            if (device == null) throw new ArgumentNullException(nameof(device));
            device.PinMode(Pin, pinMode);
            Device = device;
            Pin = pin;
        }

        internal Sensor(IGoPiGo device, Pin pin)
        {
            if (device == null) throw new ArgumentNullException(nameof(device));
            Device = device;
            Pin = pin;
        }

        public SensorStatus CurrentState => (SensorStatus)Device.DigitalRead(Pin);

        public TSensorType ChangeState(SensorStatus newState)
        {
            Device.DigitalWrite(Pin, (byte)newState);
            return this as TSensorType;
        }
    }
}
