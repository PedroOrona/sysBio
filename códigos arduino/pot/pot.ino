#include "TimerOne.h"

unsigned long time_i;
unsigned long time_f;
unsigned long result;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Timer1.initialize(4166.667);  
  Timer1.attachInterrupt(callback);
}

int value_maped;
int value;

void callback()
{
  //time_i = micros();
  value = analogRead(A0);      
  value_maped = map(value,0,1023,0,4095);
  Serial.write((unsigned char)(value_maped/64 + 128));
  Serial.write((unsigned char)(value_maped%64));
  //time_f = micros();
  //result = time_f - time_i;	
}

void loop() {

  
}
 
