#include <math.h>
#include "TimerOne.h"

void setup() {
  //configura a comunicação serial com baud rate de 9600
  Serial.begin(115200);
  //Serial.write("Gerando valores sequenciais\n");

}

unsigned int numero = 0;
//float segundos = 1/9600;
//float x = 1/9600;

void loop() {
  //exp(-numero*0.005)*sin(x)+0.1*rand();

  Serial.write(lowByte(numero));
  Serial.write(highByte(numero));
  
  numero++;
  if (numero > 4000){
    numero = 0;
  }
  delay(10);
  //x += segundos;
}
