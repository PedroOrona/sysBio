/* 
 
AUTHOR: Hazim Bitar (techbitar) 
DATE: Aug 29, 2013 
LICENSE: Public domain (use at your own risk) 
CONTACT: techbitar at gmail dot com (techbitar.com) 
EDIT FOR GALILEO: flummer (hackmeister.dk) 
 
    HC-05 GND --- Arduino GND Pin 
    HC-05 VCC (5V) --- Arduino 5V 
    HC-05 TX --- Arduino Pin 0 (hw RX) 
    HC-05 RX --- Arduino Pin1 (hw TX) 
    HC-05 Key (PIN 34) --- Arduino Pin 9 
*/  
   
void setup()  
{  
  pinMode(9, OUTPUT);  // this pin will pull the HC-05 pin 34 (key pin) HIGH to switch module to AT mode  
  digitalWrite(9, HIGH);  
  Serial.begin(9600);  
  Serial.println("Enter AT commands:");  
  Serial1.begin(38400);  // HC-05 default speed in AT command more  
}  
  
void loop()  
{  
  
  // Keep reading from HC-05 and send to Arduino Serial Monitor  
  if (Serial1.available())  
    Serial.write(Serial1.read());  
  
  // Keep reading from Arduino Serial Monitor and send to HC-05  
  if (Serial.available())  
    Serial1.write(Serial.read());  
}  
