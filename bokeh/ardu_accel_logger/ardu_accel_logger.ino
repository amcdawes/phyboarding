// Accelerometer data collection

// Upload this to an Adafruit Circuit Playground Express
// using the Arduino IDE. This code is designed to be used
// with Bokeh example accel_logger_app in this repo
// but it sends plain text via serial interface so many
// other interfaces could be built.

// Features: Click left button to record y-accel data for LENGTH samples DELAY ms apart
// Click right button to send data via serial (useful for arduino IDE monitor)

// Thanks Adafruit!

// AMCDawes 2020, for physics dashboarding talk at AAPT WM
// Based on Hello_Accelerometer and Hello_Buttons examples

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

  if (leftButtonPressed) {
    Serial.print("\nArmed: release to begin collection \n");
    CircuitPlayground.setPixelColor(0, 255, 0, 0); // 1=RED armed
    while( CircuitPlayground.leftButton() ){
      // wait while button is held
      delay(1);
    }
    // begin logging after release
    CircuitPlayground.setPixelColor(0, 0, 0, 255); // 1=BLUE logging
    Serial.print("\nActive: collecting data \n");
    for (int i = 0; i<LENGTH; i++){
      data[i] = CircuitPlayground.motionY();
      delay(DELAY);
    }
    Serial.print("\nData saved \n");
    CircuitPlayground.setPixelColor(9, 0, 255, 0); // 9=GRN Data available
    CircuitPlayground.setPixelColor(0, 0, 0, 0); // Clear active LED
  }
  if (rightButtonPressed) {
    CircuitPlayground.setPixelColor(9, 0, 30, 0); // old data still available 9=GRN/DIM
    // Read out the data
    Serial.print("DATA\n"); // TODO: do I want these tags?
    for (int i = 0; i<LENGTH; i++){
      Serial.print(data[i]);
      Serial.print(" ");
    }
    Serial.print("\nEND\n");
  }

  delay(100); // global loop delay, check buttons every 100ms
}
