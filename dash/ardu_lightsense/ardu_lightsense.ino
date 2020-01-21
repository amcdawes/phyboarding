// Light-level data collection

// Upload this to an Adafruit Circuit Playground Express
// using the Arduino IDE. This code is designed to be used
// with Plotly/Dash example live_light_app in this repo
// but it sends plain text via serial interface so many
// other interfaces could be built.

// Features: live-stream of light levels measured by the
// light sensor

// Thanks Adafruit!

// AMCDawes 2020, for physics dashboarding talk at AAPT WM


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
