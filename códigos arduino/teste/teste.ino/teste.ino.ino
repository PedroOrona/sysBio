unsigned long time1;

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  Serial.print("Time: ");
  time1 = micros();
  //prints time since program started
  Serial.println(time1);
  // wait a second so as not to send massive amounts of data
  delay(1000);
}
