namespace GoPiGo.Sensors
{
    public interface ILed
    {
        SensorStatus CurrentState { get; }
        ILed ChangeState(SensorStatus newState);
    }

    internal class Led : Sensor<ILed>, ILed
    {
        internal Led(IGoPiGo device, Pin pin) : base(device, pin, PinMode.Output)
        {
        }
    }
}
