using System;
using System.Threading.Tasks;
using Windows.Devices.Enumeration;
using Windows.Devices.I2c;
using GoPiGo.Sensors;

namespace GoPiGo
{
    public static class DeviceFactory
    {
        public static IBuildGoPiGoDevices Build = new DeviceBuilder();
    }

    public interface IBuildGoPiGoDevices
    {
        IGoPiGo BuildGoPiGo();
        IGoPiGo BuildGoPiGo(int address);
        ILed BuildLed(Pin pin);
        IUltrasonicRangerSensor BuildUltraSonicSensor(Pin pin);
    }

    internal class DeviceBuilder : IBuildGoPiGoDevices
    {
        private const string I2CName = "I2C1"; /* For Raspberry Pi 2, use I2C1 */
        private const byte GoPiGoAddress = 0x08;
        private GoPiGo _device;

        public ILed BuildLed(Pin pin)
        {
            return DoBuild(x => new Led(x, pin));
        }

        public IUltrasonicRangerSensor BuildUltraSonicSensor(Pin pin)
        {
            return DoBuild(x => new UltrasonicRangerSensor(x, pin));
        }

        private TSensor DoBuild<TSensor>(Func<GoPiGo, TSensor> factory)
        {
            var device = BuildGoPiGoImpl(GoPiGoAddress);
            return factory(device);
        }

        public IGoPiGo BuildGoPiGo()
        {
            return BuildGoPiGoImpl(GoPiGoAddress);
        }

        public IGoPiGo BuildGoPiGo(int address)
        {
            return BuildGoPiGoImpl(address);
        }

        private GoPiGo BuildGoPiGoImpl(int goPiGoAddress)
        {
            if (_device != null)
            {
                return _device;
            }

            /* Initialize the I2C bus */
            var settings = new I2cConnectionSettings(goPiGoAddress)
            {
                BusSpeed = I2cBusSpeed.StandardMode
            };

            _device = Task.Run(async () =>
            {
                var dis = await GetDeviceInfo();

                // Create an I2cDevice with our selected bus controller and I2C settings
                var device = await I2cDevice.FromIdAsync(dis[0].Id, settings);
                return new GoPiGo(device);
            }).Result;
            return _device;
        }

        private static async Task<DeviceInformationCollection> GetDeviceInfo()
        {
            //Find the selector string for the I2C bus controller
            var aqs = I2cDevice.GetDeviceSelector(I2CName);
            //Find the I2C bus controller device with our selector string
            var dis = await DeviceInformation.FindAllAsync(aqs);
            return dis;
        }
    }
}
