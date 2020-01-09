// Accelerometer data collection
// AMCDawes 2020, for physics dashboarding talk at AAPT WM
// Based on Hello_Accelerometer and Hello_Buttons examples

// Features: Click left button to record data for LENGTH samples DELAY ms apart
// Click right button to send data via serial (useful for arduino IDE monitor)
// TODO: implement dashboard that waits for serial data and plots
 
// Thanks Adafruit!

#include <Adafruit_CircuitPlayground.h>
#define LENGTH 500
#define DELAY 5

bool leftButtonPressed;
bool rightButtonPressed;

float data[LENGTH];

float X, Y, Z;

void setup() {
  Serial.begin(9600);
  CircuitPlayground.begin();
  for (int i = 0; i<LENGTH; i++){
    data[i] = 0;
  }
}

void loop() {
  leftButtonPressed = CircuitPlayground.leftButton();
  rightButtonPressed = CircuitPlayground.rightButton();

  //Serial.print("Left Button: ");
  if (leftButtonPressed) {
    Serial.print("\n Armed: release to begin collection \n");
    CircuitPlayground.setPixelColor(0, 255,   0,   0);
    while( CircuitPlayground.leftButton() ){
      // wait while button is held
      delay(1);
    }
    // begin logging after release
    CircuitPlayground.setPixelColor(0, 0,   255,   0);
    Serial.print("\n Active: collecting data \n");
    for (int i = 0; i<LENGTH; i++){
      data[i] = CircuitPlayground.motionX();
      delay(DELAY);
    }
    Serial.print("\n Data saved \n");
    CircuitPlayground.setPixelColor(9, 0,   255,   0); // Data available
    CircuitPlayground.setPixelColor(0, 0, 0, 0); // Clear active LED
  } else {
    //Serial.print("L  UP\n");
  }
  //Serial.print("   Right Button: ");
  if (rightButtonPressed) {
    CircuitPlayground.setPixelColor(9, 0, 30, 0); // old data still available
    // Read out the data
    //Serial.print("DOWN");
    Serial.print("DATA: "); // TODO: do I want these tags?
    for (int i = 0; i<LENGTH; i++){
      Serial.print(data[i]);
      Serial.print("\n");
    }
    //Serial.print(" :END\n");
  } else {
    Serial.print("  UP");    
  }
  
  delay(100);
}
