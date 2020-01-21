// A simple 1-D real-time acceleration Sensor
// This is used in the dash example accel_app.py
// but as not presented at AAPTWM2020

#include <Adafruit_CircuitPlayground.h>

float X, Y, Z;

void setup() {
  Serial.begin(2500000);
  CircuitPlayground.begin();
}

void loop() {
  //X = CircuitPlayground.motionX();
  //Y = CircuitPlayground.motionY();
  Z = CircuitPlayground.motionZ();

  //Serial.print("X: ");
  //Serial.print(X);
  //Serial.print(" Y: ");
  //Serial.print(Y);
  //Serial.print(" Z: ");
  Serial.println(Z);

  delay(10);
}
