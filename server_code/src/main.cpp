#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <Arduino.h>
#include <Wire.h>
#include "../include/json.hpp"
#include <unordered_map>
#include <string>
#include <cstdlib>

#define I2C_ADDR 0x18

// See the following for generating UUIDs:
// https://www.uuidgenerator.net/
using namespace std;
#define SERVICE_UUID "c0fe"
#define CHARACTERISTIC_UUID "3dee"
BLEServer *pServ;
BLECharacteristic *pChar;
BLEAdvertising *pAdv;
BLEService *pService;
int num_devices = 0;
using json = nlohmann::json;
string tag;
string data;
json current_user;
string request;
int sensorValue;
unsigned long time2;
bool b = false;

void requestEvents();
void receiveEvents(int);
void check_json(){
  int i =0;
  for (json::iterator it = current_user.begin(); it != current_user.end(); ++it) {
    if (it.value() != "" && it.key() != "Name"){
      i++;
    }
  if (i != 0){
    //Serial.printf("sent high signal\n");
    // Serial.printf("test here %s\n", test1.c_str());
    digitalWrite(27, HIGH);

  }
  else{
    digitalWrite(27, LOW);
  }

}
}
json createUser(string name)
{
  // create empty json and store username
  json j;
  j["Name"] = name;
  j["TempF"] = "";
  j["Condi"] = "";
  j["UVInd"] = "";
  j["Humid"] = "";
  j["CaloB"] = "";
  j["StepC"] = "";
  j["DistW"] = "";
  j["Heart"] = "";
  return j;
}
void reset_json(){
  current_user["Name"] = "";
  current_user["TempF"] = "";
  current_user["Condi"] = "";
  current_user["UVInd"] = "";
  current_user["Humid"] = "";
  current_user["CaloB"] = "";
  current_user["StepC"] = "";
  current_user["DistW"] = "";
  current_user["Heart"] = "";
  
}

/*
void storeData(json user, string userdata){
// given a refernece to a user and the data store data
string test;
int pos = userdata.find(":");
tag = userdata.substr(0,pos);
data = userdata.substr(pos + 1, userdata.length());
user[tag]= data;
/*
Serial.printf("data stored -> ");
 test = tag + data;
      for (int i = 0; i < test.length(); i++)
      {
        Serial.print(test[i]);
      }
Serial.printf("end\n");
} */
/*
class Users
{
public:
  void printUserData(json user){
       for (json::iterator it2 = user.begin(); it2 != user.end(); ++it2) {


         Serial.printf("%s - %s\n", it2.key(), it2.value());
    }
  }
 /* void addUser(json newUser)
  {
    // userMap["user1"] = user1;
    if (find_user(newUser) == NULL)
    {
    userMap[newUser["name"]] = newUser;
    }
    else
    {
      // do not add
      Serial.print("User already exists\n");
    }
  }
  void removeUser(json user)
  {
    if (find_user(user) == NULL)
    {
      // do not remove
    }
    else
    {
      // remove
    }
  }

  json find_user(json user)
  {
    unordered_map<std::string, json>::iterator it;
    it = userMap.find(user["name"]);
    // user found
    if (it != userMap.end())
    {
      return it->second;
    }
    else
    { // user not found
      return NULL;
    }
  }

private:
  // vector<*json> userList;
  unordered_map<string, json> userMap;
};

Users master;
*/
class MyCallbacks : public BLECharacteristicCallbacks
{
  void onWrite(BLECharacteristic *pCharacteristic)
  {
    std::string value = pCharacteristic->getValue();

    if (value.length() > 0)
    {
      // Serial.print("*********");
      // Serial.print("New value: ");
      for (int i = 0; i < value.length(); i++)
      {
        Serial.print(value[i]);
      }

      Serial.println();
      // Serial.println("*********");
    }
    if (value == "Connected")
    {

      Serial.printf("created user\n");
    }
    else if(value == "Disconnected"){
     // current_user = createUser("User1");
     Serial.printf("userleft\n");
     reset_json();
      digitalWrite(27, LOW);
    }
    else
    {
      string test, test2;
      int pos = value.find(":");
      tag = value.substr(0, pos);
      data = value.substr(pos + 2, value.length());
      
      if (tag == "NewName"){
        tag = "Name";
      }
      current_user[tag] = data;
      test = current_user[tag];

      Serial.printf("Test Data -%s-, -%s- \n", test.c_str(), tag.c_str());
      //  test = current_user[tag];
      //  Serial.printf(" ---Test This %s- %s---\n", tag.c_str(), test.c_str());
    }
  }
};

void setup()
{
  // const char* sensor_program_command = "/path/to/your/sensor_program";
  Serial.begin(115200);
  current_user = createUser("User1");
  pinMode(34, INPUT);
  pinMode(32, OUTPUT);
  pinMode(27, OUTPUT);

  digitalWrite(32, HIGH);
  digitalWrite(27, LOW);

  BLEDevice::init("ESP32-BLE-Server");
  pServ = BLEDevice::createServer();
  pService = pServ->createService(SERVICE_UUID);

  pChar = pService->createCharacteristic(
      CHARACTERISTIC_UUID,
      BLECharacteristic::PROPERTY_READ |
          BLECharacteristic::PROPERTY_WRITE);

  pChar->setCallbacks(new MyCallbacks());

  pChar->setValue("Device Connected");
  pService->start();

  pAdv = pServ->getAdvertising();
  pAdv->start();

  Wire.begin(I2C_ADDR);
  Wire.onRequest(requestEvents);
  Wire.onReceive(receiveEvents);
  request = "";
}

void loop()
{
  string test1;

  test1 = current_user["Heart"];
  check_json();
  // if (test1 != "")
  // {
  //   Serial.printf("DATA PIN HIGH\n");
  //   // Serial.printf("test here %s\n", test1.c_str());
  //   digitalWrite(27, HIGH);
  // }
  // else
  // {

  //   digitalWrite(27, LOW);
  // }

  delay(1000);
  num_devices = pServ->getConnectedCount();
  // Serial.printf("%d\n", num_devices);
  if (num_devices == 0)
  {
    pAdv->stop();
    pAdv->start();
  }

  if (digitalRead(34) == HIGH)
  {
    Serial.printf("-- %lu -- Motion Deteced!\n ", (millis() / 1000));
    digitalWrite(32, HIGH);
  }
  else
  {
    digitalWrite(32, LOW);
   // Serial.printf("------\n");
  }
  time2 = millis();
  time2 = time2 / 1000;

  sensorValue = analogRead(25);

  // Convert the analog value to voltage (assuming 3.3V reference)
  float voltage = sensorValue * (3.3 / 4095.0);

  // Convert voltage to temperature using LM35 formula (10mV per degree F)
  float temperatureF = voltage * 100.0; // 10mV per degree Celsius
                                        // Serial.printf("RoomTemp - %f\n");
                                   //     if (temperatureF != 0) Serial.printf("RoomTemp - %f\n");
}

void requestEvents()
{

  string data2;
  float test;
  int test1;
  char byte;
  Serial.printf("REQUEST\n");
  data2 = current_user[request];
  test = std::stof(data2);
  test1 = (int) test;
  data2 = to_string(test1);
  Serial.printf("msg len %d\n", data2.length());
  Serial.printf("msg- %s\n", data2.c_str());
  Wire.write((char)data2.length());
  for (int i = 0; i < data2.length(); i++)
  {
    Serial.printf(" -%d-",i);
    Wire.write(data2[i]);
    
  }
  Serial.printf("\n");
  if (request != "Name"){
  current_user[request] = "";
  }


}
void receiveEvents(int num)
{

  char c;
  request.clear();
  Serial.printf("RECIEVE\n");

  while (Wire.available())
  {

    c = Wire.read();
    if (c != 0)
    {
      request.push_back(c);
    //  Serial.printf("printing char  %d\n", c);
    }
  }
  Serial.printf("STRING - %s\n", request.c_str());
  
}