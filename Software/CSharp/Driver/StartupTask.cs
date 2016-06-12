using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net.Http;
using System.Threading;
using Windows.ApplicationModel.Background;
using Windows.System.Threading;
using GoPiGo;

// The Background Application template is documented at http://go.microsoft.com/fwlink/?LinkID=533884&clcid=0x409

namespace Driver
{
    public sealed class StartupTask : IBackgroundTask
    {
        private BackgroundTaskDeferral _deferral;
        private IGoPiGo _goPiGo;
        private ThreadPoolTimer _timer;
        private int _count;

        public void Run(IBackgroundTaskInstance taskInstance)
        {
            _deferral = taskInstance.GetDeferral();

            _goPiGo = DeviceFactory.Build.BuildGoPiGo();

            _timer = ThreadPoolTimer.CreatePeriodicTimer(TurnLeftGoForward, TimeSpan.FromSeconds(10));
        }

        private void TurnLeftGoForward(ThreadPoolTimer timer)
        {
            if (_count == 0)
            {
                _goPiGo.MotorController().MoveForward();
            }

            if (_count == 1)
            {
                _goPiGo.MotorController().Stop();
            }

            if (_count == 2)
            {
                _goPiGo.MotorController().RotateLeft();
            }

            if (_count == 3)
            {
                _goPiGo.MotorController().Stop();
            }

            if (_count == 4)
            {
                _timer.Cancel();
                _deferral.Complete();
            }

            _count++;

            //_goPiGo.MotorController().Stop();

            //if (_count++ > 20)
            //{
            //    _timer.Cancel();
            //    _deferral.Complete();
            //    return;
            //}

            //if (_count % 3 == 0)
            //{
            //    _goPiGo.MotorController().MoveForward();
            //}

            //if (_count % 4 >= 0)
            //{
            //    _goPiGo.MotorController().RotateLeft();
            //}
        }
    }
}
