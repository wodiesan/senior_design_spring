/*
@author:     Sze 'Ron' Chau
@source:     https://github.com/wodiesan/senior_design_spring
@Desc:       Adafruit Analog Light Sensor, modified by Ron Chau.
@Misc:       This version uses a stand-alone ATtiny85.

 1. Connect sensor output to Analog Pin 0
 2. Connect 5v to VCC and GND to GND
 3. Connect 3.3v to the AREF pin
*/

//int led1 = 2;          // LED connected to digital pin 2 (Uno)
//int sensorPin = A0;    // Sensor connected to pin A0 (Uno)

int led1 = 1;          // LED connected to digital pin 1 (physical pin 6)
int led2 = 3;          // LED connected to digital pin 3 (physical pin 2)
int led3 = 4;          // LED connected to digital pin 4 (physical pin 3)
int sensorPin = A1;    // Sensor connected to pin A1 (phys pin 7)

float rawRange = 1024; // 3.3v
float logRange = 5.0; // 3.3v = 10^5 lux

// Clear day sunset value chosen to test light sensing feature.
float lightLimit = 300;

void setup()
{
  analogReference(EXTERNAL); //
  //Serial.begin(9600);
  //Serial.println("Adafruit Analog Light Sensor Test");

  // LED pins
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
}

void loop()
{
  // Read the raw value from the sensor:
  int rawValue = analogRead(sensorPin);

  //Serial.print("Raw = ");
  //Serial.print(rawValue);
  //Serial.print(" - Lux = ");
  //Serial.println(RawToLux(rawValue));
  int luxValue = (RawToLux(rawValue));
  //Serial.print("luxVal = ");
  //Serial.println(luxValue);
  delay(1000);

  // LEDS on if lux less than or equal.
  if(luxValue <= lightLimit){
    digitalWrite(led1, HIGH);   // LEDs on
    digitalWrite(led2, HIGH);
    digitalWrite(led3, HIGH);
  }
  else{
    digitalWrite(led1, LOW);   // LEDs off
    digitalWrite(led2, LOW);
    digitalWrite(led3, LOW);
  }
  //delay(1000);
}

float RawToLux(int raw)
{
  float logLux = raw * logRange / rawRange;
  return pow(10, logLux);
}
