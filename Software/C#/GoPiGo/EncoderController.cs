namespace GoPiGo
{
    public interface IEncoderController
    {
        IEncoderController SetEncoderTargetingOn(State motorOneState, State motorTwoStatem, int target);
        int ReadEncoder(Motor motor);
        IEncoderController EnableEncoders();
        IEncoderController DisableEncoders();
    }

    public class EncoderController : IEncoderController
    {
        private GoPiGo goPiGo;

        public EncoderController(GoPiGo goPiGo)
        {
            this.goPiGo = goPiGo;
        }

        public IEncoderController SetEncoderTargetingOn(State motorOneState, State motorTwoState, int target)
        {
            var motorSelect = (int)motorOneState * 2 + (int)motorTwoState;
            goPiGo.RunCommand(Commands.SetEncoderTargeting, (byte)motorSelect, (byte)(target / 256), (byte)(target % 256));
            return this;
        }

        public int ReadEncoder(Motor motor)
        {
            var buffer = new[] { (byte)Commands.ReadEncoder, (byte)motor, Constants.Unused, Constants.Unused };

            goPiGo.DirectAccess.Write(buffer);
            goPiGo.DirectAccess.Read(buffer);

            int encoder = buffer[1] * 256 + buffer[2];
            return encoder;
        }

        public IEncoderController EnableEncoders()
        {
            goPiGo.RunCommand(Commands.EnableEncoder);
            return this;
        }

        public IEncoderController DisableEncoders()
        {
            goPiGo.RunCommand(Commands.DisableEncoder);
            return this;
        }
    }
}
