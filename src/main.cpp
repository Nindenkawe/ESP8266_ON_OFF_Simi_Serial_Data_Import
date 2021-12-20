#include <Arduino.h>
#include <ArduinoJson.h>
#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>
#include <Wire.h>

#define SS_PIN 10
#define RST_PIN 9
//......................................................................................................................................................
MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.
Servo myservo;  // create servo object to control a servo
                // twelve servo objects can be created on most boards
int pos = 0;    // variable to store the servo position
//............................
void setup(){
  Serial.begin(115200);   // Initiate a serial communication
  SPI.begin();      // Initiate  SPI bus
  mfrc522.PCD_Init();   // Initiate MFRC522
  Serial.println("Approximate your card to the reader...");
  Serial.println("....||........||........||..............||..........||..........||...||.............||....................||");
//.......................................................................................................................................................
  myservo.attach(8);
//.......................................................................................................................................................
 
}
// Look for new cards
void loop()
  {
if ( ! mfrc522.PICC_IsNewCardPresent())
  {
    return;
  }
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) 
  {
  return;
  }
  //.......................................................................................................................................................
    // Look for new cards
if ( ! mfrc522.PICC_IsNewCardPresent()) 
{
  return;
}
  // Select one of the cards
if ( ! mfrc522.PICC_ReadCardSerial()) 
{
  return;
}
  //Show UID on serial monitor
  Serial.print("UID tag :");
  String content= "";
  byte letter;
for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
    Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(mfrc522.uid.uidByte[i], HEX);
    content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
    content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
    Serial.println();
    Serial.print("Message : ");
    content.toUpperCase();
if(content.substring(1) == "CC 47 37 18") //change here the UID of the card/cards that you want to give access
{
    Serial.println("Authorized access8");
    
    for (pos = 0; pos <= 90; pos += 1){ // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
  delay (3000);

  for (pos = 90; pos >= 0; pos -= 1){ // goes from 180 degrees to 0 degrees
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
  
}

else if (content.substring(1) == "4A BF 71 AE") //change here the UID of the card/cards that you want to give access
  {
    Serial.println("Authorized access7");
  
  }
 
else{
    Serial.println(" Access denied");
    delay(1000);
  }
}