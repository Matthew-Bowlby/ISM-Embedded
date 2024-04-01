/*

Have Nano request specific item - In receiveEvents Nano sends a thing like heartbeat or whatever
                                - ESP receives item name
Send Item to Nano - In requestEvents send the value of a given item
                  - Nano receives value of item requested


*/

#include <Arduino.h>
#include <Wire.h>
#include <unordered_map>

using namespace std;

#define I2C_ADDR 0x18

void requestEvents();
void receiveEvents(int);

unordered_map <string, int> info_map;     // store val with corresponding string - ("heartrate", 60)
unordered_map <string, int>::iterator it;
string request;

void setup() {
  Wire.begin(I2C_ADDR);
  Serial.begin(9600);
  Wire.onRequest(requestEvents);
  Wire.onReceive(receiveEvents);
  request = "";
}

void loop() {

}

void requestEvents() {
  int data = 0;
  char byte;

  it = info_map.find(request);
  data = it->second;

  do {
    byte = data & 0xFF;
    data >> 8;
    Wire.write(byte);
  } while (data != 0);
}

void receiveEvents(int num) {
  char c;
  request.clear();
  while (Wire.available()){
    c = Wire.read();
    request.push_back(c);
  }

}
