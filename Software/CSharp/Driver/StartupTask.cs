using Windows.ApplicationModel.Background;
using GoPiGo;
using GoPiGo.Sensors;

// The Background Application template is documented at http://go.microsoft.com/fwlink/?LinkID=533884&clcid=0x409

namespace Driver
{
    public sealed class StartupTask : IBackgroundTask
    {
        private readonly IBuildGoPiGoDevices _deviceFactory = DeviceFactory.Build;

        public void Run(IBackgroundTaskInstance taskInstance)
        {
            var goPiGo = _deviceFactory.BuildGoPiGo();

            var leftLed = _deviceFactory.BuildLed(Pin.LedLeft);
            var rightLed = _deviceFactory.BuildLed(Pin.LedRight);

            //leftLed.ChangeState(SensorStatus.On);
            //rightLed.ChangeState(SensorStatus.On);

            leftLed.ChangeState(SensorStatus.Off);
            rightLed.ChangeState(SensorStatus.Off);

            var version = goPiGo.GetFirmwareVersion();
            //goPiGo.MotorController().MoveForward();
            goPiGo.MotorController().Stop();

        }
    }
}
