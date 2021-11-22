#include <Arduino.h>
#include <ArduinoJson.h>
#include <SPI.h>
#include <HCSR04.h>
#include <Wire.h>

//define Pins
#define trigPin1 11
#define echoPin1 12

long duration, distance, RightSensor;
String message = "";
bool messageReady = false;

void setup(){
    Serial.begin(115200);
    Serial.print("Zone A1 online");

pinMode(trigPin1, OUTPUT);
pinMode(echoPin1, INPUT);

}

void SonarSensor(int trigPin,int echoPin){
    
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration/2) / 29.1;
  delay(1500);
}

void loop()
  {
    // Monitor serial communication
  while(Serial.available()) {
    message = Serial.readString();
    messageReady = true;
  }
  // Only process message if there's one
  if(messageReady) {
    // The only messages we'll parse will be formatted in JSON
    DynamicJsonDocument doc(1024); // ArduinoJson version 6+
    // Attempt to deserialize the message
    DeserializationError error = deserializeJson(doc,message);
    if(error) {
      Serial.print(F("deserializeJson() failed: "));
      Serial.println(error.c_str());
      messageReady = false;
      return;
    }
    if(doc["type"] == "request") {
      doc["type"] = "response";
      // Get data from sensors
      doc["distance"] = digitalRead(trigPin1);
      doc["duration"] = digitalRead(echoPin1);
      serializeJson(doc,Serial);
    }
    messageReady = false;
  } 
  SonarSensor(trigPin1, echoPin1);
  RightSensor = distance;
  Serial.print(RightSensor);
  Serial.print(" - ");

if (RightSensor > 100){
    //Serial print
    Serial.println("1 Slots Free, || Parking Available");
    delay(1500);
  }
else if(RightSensor <= 100){
    //Serial print
    Serial.println("0 Slots Free, || Parking full");
    delay(1500);
  }
else{
    //Serial print
    Serial.println("Out of Service");
    delay(1500);
  }
}