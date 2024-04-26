#include <Arduino.h>
uint8_t state;
// put function declarations here:
int sensorValue;

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(115200);

  pinMode(34, INPUT);
  pinMode(32, OUTPUT);
   pinMode(27, OUTPUT);

  state = HIGH;
  digitalWrite(32, HIGH);
   digitalWrite(27, LOW);
}
unsigned long time2;
void loop()
{
   
  /*
  if (state == HIGH) {
    digitalWrite(32, LOW);
    state = LOW;
  }
  else {
    digitalWrite(32, HIGH);
    state = HIGH;
  }
  */
  // put your main code here, to run repeatedly:
  if (digitalRead(34) == HIGH)
  {

    Serial.printf("-- %lu -- Motion Deteced!\n ", (millis() / 1000));
    digitalWrite(32, HIGH);
    /*
    if (state == LOW)
    {
      digitalWrite(32, HIGH);
      state = HIGH;
    }
    */
  }
  else
  {
    digitalWrite(32, LOW);
    /*
    if (state == HIGH)
    {
      digitalWrite(32, LOW);
      state = LOW;
    }
    */
    //    Serial.printf(".\n");
    Serial.printf("------\n");
  }
  time2 = millis();
  time2 = time2/1000;
  if (time2 % 30 == 0 && time != 0){
    digitalWrite(27,HIGH);
    
  } 
  
  sensorValue = analogRead(25);

  // Convert the analog value to voltage (assuming 3.3V reference)
  float voltage = sensorValue * (3.3 / 4095.0);

  // Convert voltage to temperature using LM35 formula (10mV per degree F)
  float temperatureF = voltage * 100.0; // 10mV per degree Celsius
  /*
  Serial.print("Temperature: ");
  Serial.print(temperatureF);
  Serial.println(" °F\n");
*/
  delay(1000);
}
