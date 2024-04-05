#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <Arduino.h>
#include <Wire.h>
#include <json.hpp>
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

void requestEvents();
void receiveEvents(int);


json createUser(string name){
// create empty json and store username
json j;
j["name"] = name;
return j;

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
      //Serial.print("New value: ");
      for (int i = 0; i < value.length(); i++)
      {
        Serial.print(value[i]);
      }

      Serial.println();
      // Serial.println("*********");
    }
    if (value == "Connected"){
     current_user = createUser("User1");

     Serial.printf("created user\n");
    }
    else{
    string test;
    
    int pos = value.find(":");
    tag = value.substr(0,pos);
    data = value.substr(pos + 1, value.length());
    current_user[tag]= data;
      
     // Serial.printf("Test Data -%s-\n", current_user[tag]);
    //  test = current_user[tag];
    //  Serial.printf(" ---Test This %s- %s---\n", tag.c_str(), test.c_str());
    }

  }
};

void setup()
{
 // const char* sensor_program_command = "/path/to/your/sensor_program";
  Serial.begin(115200);

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

  /* if (theServer->getConnectedCount() < num_devices)
   {
     Serial.print("*********\n");
     Serial.print("A device has connected.");
     Serial.print("*********\n");
   }
   if (theServer->getConnectedCount() > num_devices)
   {
     Serial.print("*********\n");
     Serial.print("A device has disconnected.");
     Serial.print("*********\n");
   }*/
  delay(2000);
  num_devices = pServ->getConnectedCount();
  //Serial.printf("%d\n", num_devices);
  if (num_devices == 0) 
  {
    pAdv->stop();
    pAdv->start();


  }
}
void requestEvents() {
  string data2;
  char byte;

  data2 = current_user[request];
  
  for(int i = 0; i < data2.length(); i++){
       Wire.write(data2[i]);
  }

}
void receiveEvents(int num) {
  char c;
  request.clear();
  while (Wire.available()){
    c = Wire.read();
    request.push_back(c);
  }

}