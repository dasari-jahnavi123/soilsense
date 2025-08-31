#include "DHT.h"

#define DHTPIN 2         // DHT11 connected to digital pin D2
#define DHTTYPE DHT11    // DHT11 (use DHT22 if you have that)
DHT dht(DHTPIN, DHTTYPE);

int soilPin = A0;  // Soil Moisture AO connected to A0

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  // 🌡️ Read temperature & humidity
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature(); // Celsius

  // 🌱 Read soil moisture
  int soilValue = analogRead(soilPin); // Raw value (0–1023)
  int soilPercent = map(soilValue, 1023, 0, 0, 100); // Convert to %

  // Check if DHT read failed
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // 📊 Print all values together
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print("°C | Humidity: ");
  Serial.print(humidity);
  Serial.print("% | Soil Moisture: ");
  Serial.print(soilPercent);
  Serial.println("%");

  delay(2000); // wait 2 sec
}