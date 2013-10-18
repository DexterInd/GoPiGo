//Code for testing interrupts for the encoder signal
volatile int state = LOW;
volatile int s=0;
void setup()
{
  Serial.begin(115200);
  attachInterrupt(0, step, RISING);
}
void loop()
{
  if(s%36==0)
    Serial.println(s/36);
}
void step()
{
  s++;
}
