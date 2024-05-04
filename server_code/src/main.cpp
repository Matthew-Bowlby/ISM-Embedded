#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <Arduino.h>
#include <Wire.h>
#include "../include/json.hpp"
#include <string>
#include <cstdlib>
#include "../include/aes.hpp"
#define I2C_ADDR 0x18

// See the following for generating UUIDs:
// https://www.uuidgenerator.net/
// using namespace CryptoPP;
using namespace std;
#define SERVICE_UUID "c0fe"
#define CHARACTERISTIC_UUID "3dee"
BLEServer *pServ;
BLECharacteristic *pChar;
BLEAdvertising *pAdv;
BLEService *pService;
int num_devices = 0;
using json = nlohmann::json;
string tag;                       // variable for accessing json
string data;                      // variable for storing data to json
json current_user;                // json for storing user data
string request;                   // request string for i2c
int sensorValue;                  // int for reading analog output for temp sensor
unsigned long time2;              

// using namespace CryptoPP;
void requestEvents();
void receiveEvents(int);
// Check the Json for any available data to send by checking if it has set to any but empty
// The one exception is the name since the facial recognition database is base on username alone
void check_json()
{
  int i = 0;
  for (json::iterator it = current_user.begin(); it != current_user.end(); ++it)
  {
    if (it.value() != "" && it.key() != "Name" && it.key() != "Temp" )
    {
      i++;
    }
    if (i != 0)
    {
      digitalWrite(27, HIGH);
      digitalWrite(27, LOW);
    }
    else
    {
      digitalWrite(27, LOW);
    }
  }
}
json createUser(string name)
{
  // create empty json and store username
  json j;
  j["Name"] = name; // default user name User1
  j["TempF"] = "";
  j["Condi"] = "";
  j["UVInd"] = "";
  j["Humid"] = "";
  j["CaloB"] = "";
  j["StepC"] = "";
  j["DistW"] = "";
  j["Heart"] = "";
  j["Bright"] = "";
  j["Temp"] = "";
  return j;
}
void reset_json()
{
  // Reset all values only if no user is connected
  current_user["Name"] = "";
  current_user["TempF"] = "";
  current_user["Condi"] = "";
  current_user["UVInd"] = "";
  current_user["Humid"] = "";
  current_user["CaloB"] = "";
  current_user["StepC"] = "";
  current_user["DistW"] = "";
  current_user["Heart"] = "";
  current_user["Bright"] = "";
  current_user["Temp"] = "";
}

// Convert the encrypted AES string to byte array for AES decryption
void hexStringToByteArray(const std::string &hexString, uint8_t *byteArray)
{

   size_t i;
  size_t length = hexString.length();
  for (i = 0; i < length; i += 2)
  {
    // Extract two characters from the hexadecimal string and convert them to a byte
    std::string byteString = hexString.substr(i, 2);
    byteArray[i / 2] = static_cast<uint8_t>(std::stoi(byteString, nullptr, 16));
  }
  
}
// Convert the byte array back to string in order to store it into the JSON
std::string byteArrayToString(const unsigned char* byteArray, size_t length) {
    string s;
    for (int i = 0; byteArray[i] != '+'; i++) {
      s.push_back(byteArray[i]);
    }
    return s;
}

// When anything is written from the users phone it is read in a callback in the background
// This function also simultaneuosly handles the decryption and storage of the information sent
class MyCallbacks : public BLECharacteristicCallbacks
{
  void onWrite(BLECharacteristic *pCharacteristic)
  {
    struct AES_ctx ctx;
    std::string value = pCharacteristic->getValue();
    string value1;
    uint8_t key[] = { 49, 56, 67, 51, 68, 53, 51, 49, 70, 49, 48, 54, 54, 70, 66, 68 };

    uint8_t iv[] = { 67, 52, 68, 52, 67, 52, 50, 57, 65, 48, 52, 54, 65, 68, 68, 68 };
    uint8_t in[100];
    

    // change encrypted hex string to byte array
    hexStringToByteArray(value, in);
  
    // decrypt
    AES_init_ctx_iv(&ctx, key, iv);

    AES_CBC_decrypt_buffer(&ctx, in, 64);

    // convert byte array plaintext back to string
    value1 = byteArrayToString(in, 64);

    if (!value1.empty())
    {
      if (value1.length() > 0)
      {
        for (int i = 0; i < value1.length(); i++)
        {
          Serial.print(value1[i]);
        }

        Serial.println();
      }
      if (value1 == "Connected")
      {
        Serial.printf("created user\n");
      }
      else if (value1 == "Disconnected")
      {
        // notify disconnection and reset the json so that it does not send unidentified data
        Serial.printf("user left\n");
        reset_json();
        digitalWrite(27, LOW);
      }
      else
      {
        string test, test2;
        float dumb;
        int dumb3;
        // parse the decrypted data into tag and data
        int pos = value1.find(":");
        tag = value1.substr(0, pos);
        data = value1.substr(pos + 2, value1.length());

        // changes the username but keeps reference to the same data 
        if (tag == "NewName")
        {
          tag = "Name";
        }
        if (tag == "Heart")
        {
          // truncates the float representation of the heartrate
          dumb = stof(data);
          dumb3 = (int)dumb;
          data = to_string(dumb3);
     
        }
        current_user[tag] = data;
        test = current_user[tag];

     
      }
    }
    else
    {
     // do nothing
    }
  }
};

// Set up bluetooth and all of the peripheral components 
void setup()
{
  // const char* sensor_program_command = "/path/to/your/sensor_program";
  Serial.begin(115200);
  current_user = createUser("User1"); // sets up default user with no data
  pinMode(34, INPUT);
  pinMode(32, OUTPUT);
  pinMode(27, OUTPUT);

  digitalWrite(32, HIGH);
  digitalWrite(27, LOW);

  BLEDevice::init("ESP32-BLE-Server"); // how the device will appear by name 
  pServ = BLEDevice::createServer();
  pService = pServ->createService(SERVICE_UUID);


  // set up the server and start advertising its services and connection requirements via the characteristic ID
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
  check_json(); // check if any data is to be sent

  delay(1000);
  num_devices = pServ->getConnectedCount();

  // reset and readvertise services if someone disconnects
  if (num_devices == 0)
  {
    pAdv->stop();
    pAdv->start();
  }

  // Send signal to nano if motion is detected to activate its functions
  if (digitalRead(34) == HIGH)
  {
    Serial.printf("-- %lu -- Motion Deteced!\n ", (millis() / 1000));
    digitalWrite(32, HIGH);
  }
  else
  {
    // other wise no one is present so do nothing
    digitalWrite(32, LOW);

  }
  time2 = millis();
  time2 = time2 / 1000;

  // get value from temp sensor
  sensorValue = analogRead(25);

  // Convert the analog value to voltage (assuming 3.3V reference)
  float voltage = sensorValue * (3.3 / 4095.0);

  // Convert voltage to temperature using LM35 formula (10mV per degree F)
  float temperatureC = voltage / .01; // 10mV per degree Celsius
                                   
  // Send the ambient temp reading as long as a user is connected
  temperatureC += 10;
  if (current_user["Name"] != ""){ 
    current_user["Temp"] = to_string(temperatureC);
 
  }
}

void requestEvents()
{

  string data2;
  char byte;

  // access data stored in json to send over i2c
  data2 = current_user[request];

  // Send data string across i2c data line
  // data is of format: [data_string_size, data_bytes]
  Wire.write((char)data2.length());
  for (int i = 0; i < data2.length(); i++)
  {

    Wire.write(data2[i]);
  }
  // since the name is the key to the data base nano side we want to retain the name for data updates.
  // since the temp is updated constantly there is no need to reset
  if (request != "Name" && request != "Temp")
  {
    current_user[request] = "";
  }
}

void receiveEvents(int num)
{
  char c;

  // Clears request and adds request by byte onto request string
  request.clear();

  while (Wire.available())
  {
    c = Wire.read();
    if (c != 0)
    {
      request.push_back(c);

    }
  }
 
}
