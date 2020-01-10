#include <Adafruit_CircuitPlayground.h>

int value;

void setup() {
  Serial.begin(2500000);
  CircuitPlayground.begin();
}

void loop() {
  value = CircuitPlayground.lightSensor();
  
  //Serial.print("Light Sensor: ");
  Serial.println(value);
  
  delay(10);
}
