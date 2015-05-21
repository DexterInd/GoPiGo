using System;

namespace GoPiGo
{
    public interface IMotorController
    {
        IMotorController MoveForward();
        IMotorController MoveForwardNoPid();
        IMotorController MoveBackward();
        IMotorController MoveBackwardNoPid();
        IMotorController MoveLeft();
        IMotorController RotateLeft();
        IMotorController MoveRight();
        IMotorController RotateRight();
        IMotorController Stop();
        IMotorController IncreaseSpeedBy10();
        IMotorController DecreaseSpeedBy10();
        IMotorController ControlMotorOne(int direction, int speed);
        IMotorController RotateServo(int degrees);
        IMotorController EnableServo();
        IMotorController DisableServo();
        IMotorController SetLeftMotorSpeed(int speed);
        IMotorController SetRightMotorSpeed(int speed);
    }

    public class MotorController : IMotorController
    {
        internal MotorController(IGoPiGo goPiGo)
        {
            if (goPiGo == null) throw new ArgumentNullException(nameof(goPiGo));
            GoPiGo = goPiGo;
        }

        public IGoPiGo GoPiGo { get;private set; }


        public IMotorController MoveForward()
        {
            GoPiGo.RunCommand(Commands.MoveForward);
            return this;
        }

        public IMotorController MoveForwardNoPid()
        {
            GoPiGo.RunCommand(Commands.MoveForwardNoPid);
            return this;
        }

        public IMotorController MoveBackward()
        {
            GoPiGo.RunCommand(Commands.MoveBackward);
            return this;
        }

        public IMotorController MoveBackwardNoPid()
        {
            GoPiGo.RunCommand(Commands.MoveBackwardNoPid);
            return this;
        }

        public IMotorController MoveLeft()
        {
            GoPiGo.RunCommand(Commands.MoveLeft);
            return this;
        }

        public IMotorController RotateLeft()
        {
            GoPiGo.RunCommand(Commands.RotateLeft);
            return this;
        }

        public IMotorController MoveRight()
        {
            GoPiGo.RunCommand(Commands.MoveRight);
            return this;
        }

        public IMotorController RotateRight()
        {
            GoPiGo.RunCommand(Commands.RotateRight);
            return this;
        }

        public IMotorController Stop()
        {
            GoPiGo.RunCommand(Commands.Stop);
            return this;
        }

        public IMotorController IncreaseSpeedBy10()
        {
            GoPiGo.RunCommand(Commands.IncreaseSpeedBy10);
            return this;
        }

        public IMotorController DecreaseSpeedBy10()
        {
            GoPiGo.RunCommand(Commands.DecreaseSpeedBy10);
            return this;
        }

        public IMotorController ControlMotorOne(int direction, int speed)
        {
            GoPiGo.RunCommand(Commands.MotorOne, (byte)direction, (byte)speed);
            return this;
        }

        public IMotorController ControlMotorTwo(int direction, int speed)
        {
            GoPiGo.RunCommand(Commands.MotorTwo, (byte)direction, (byte)speed);
            return this;
        }

        public IMotorController RotateServo(int degrees)
        {
            GoPiGo.RunCommand(Commands.RotateServo, (byte)degrees);
            return this;
        }

        public IMotorController EnableServo()
        {
            GoPiGo.RunCommand(Commands.EnableServo);
            return this;
        }

        public IMotorController DisableServo()
        {
            GoPiGo.RunCommand(Commands.DisableServo);
            return this;
        }

        public IMotorController SetLeftMotorSpeed(int speed)
        {
            speed = Math.Min(speed, 255);
            GoPiGo.RunCommand(Commands.SetLeftMotorSpeed, (byte)speed);
            return this;
        }

        public IMotorController SetRightMotorSpeed(int speed)
        {
            speed = Math.Min(speed, 255);
            GoPiGo.RunCommand(Commands.SetRightMotorSpeed, (byte)speed);
            return this;
        }

        public IMotorController SetSpeed(int speed)
        {
            SetLeftMotorSpeed(speed);
            SetRightMotorSpeed(speed);
            return this;
        }
    }
}
