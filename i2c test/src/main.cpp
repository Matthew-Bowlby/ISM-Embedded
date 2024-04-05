#include <Arduino.h>
#include <Wire.h>

#define I2C_ADDR 0x18

int n = 0;
std::string val;

void requestEvents();
void receiveEvents(int);

void setup() {
  // put your setup code here, to run once:
  Wire.begin(I2C_ADDR);
  Serial.begin(9600);
  Wire.onRequest(requestEvents);
  Wire.onReceive(receiveEvents);
}

void loop() {
  // put your main code here, to run repeatedly:
  //Serial.println("hello");

  //delay(100);
}

void requestEvents() {
  std::string s = "hello";


  for (int i = 0; i < 32; i++) {
      Wire.write(1);
  }
  for (int i = 0; i < 32; i++) {
      Wire.write(2);
  }
}

void receiveEvents(int num) {
  char c;
  //Serial.print('\n');
  while (Wire.available()){
    c = Wire.read();
    if (c != 0) Serial.print(c);
  }
  //Serial.print('\n');
  //Serial.println(num);
  //Serial.print(F(" new recieved value : "));
  //Serial.println(n);
}
