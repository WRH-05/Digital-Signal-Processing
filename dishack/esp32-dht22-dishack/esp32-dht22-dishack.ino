/**
   ESP32 + DHT22 + I2C LCD + Buzzer + ThingSpeak Integration with Storage, 
   Shelf Life Monitoring, and Expired Bag Removal

   - Reads temperature and humidity every 2 seconds.
   - Updates LCD, Serial Monitor, and buzzer immediately.
   - Every 15 seconds, averages sensor data and sends:
       Field 1: Average Temperature
       Field 2: Average Humidity
       Field 3: Total Blood Bag Count (Inventory)
       Field 4: Count of Expired Blood Bags
   - Blood bags are added via a simulated button (on BUTTON_ADD).
   - A separate button (BUTTON_REMOVE) removes expired blood bags from inventory.
   - Shelf life is accelerated for simulation (e.g., 42 seconds = 42 days).
*/

#include "DHTesp.h"
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <WiFi.h>
#include <ThingSpeak.h>

// WiFi credentials – update with your network details
const char* ssid     = "Wokwi-GUEST";
const char* password = "";

// ThingSpeak channel settings – update with your channel number and Write API key
unsigned long myChannelNumber = 2850392;   // Replace with your channel number
const char* myWriteAPIKey   = "NGNBSNYJZKBUHNAZ";

// Define pins for components
const int DHT_PIN      = 15;  // DHT22 sensor pin
const int BUZZER_PIN   = 13;  // Buzzer pin
const int BUTTON_ADD   = 12;   // Virtual button pin to add a blood bag (simulate input; active LOW)
const int BUTTON_REMOVE= 14;   // Virtual button pin to remove expired blood bags (active LOW)

DHTesp dhtSensor;
LiquidCrystal_I2C lcd(0x27, 16, 2); // Adjust I2C address if needed

// Safe range thresholds for blood storage conditions
const float TEMP_LOW   = 1.0;
const float TEMP_HIGH  = 6.0;
const float HUMID_LOW  = 40.0;
const float HUMID_HIGH = 60.0;

WiFiClient client;

// Variables for averaging sensor readings over 15 seconds
unsigned long lastThingSpeakUpdate = 0;
float temperatureSum = 0.0;
float humiditySum    = 0.0;
int sampleCount      = 0;

// Shelf life settings (accelerated for simulation)
// For example, consider 42 seconds to represent 42 days.
const unsigned long SHELF_LIFE = 42;

// Structure for blood bag info
struct BloodBag {
  String id;
  unsigned long storedTime; // using millis() for simulation
};

const int MAX_BLOODBAGS = 20;
BloodBag bloodBags[MAX_BLOODBAGS];
int bloodBagCount = 0;

// Function to add a new blood bag
void addBloodBag(String id) {
  if (bloodBagCount < MAX_BLOODBAGS) {
    bloodBags[bloodBagCount].id = id;
    bloodBags[bloodBagCount].storedTime = millis();
    bloodBagCount++;
    Serial.println("Added blood bag: " + id);
  }
}

// Function to remove expired blood bags
void removeExpiredBags() {
  unsigned long currentTime = millis();
  int removedCount = 0;
  // Process the array and remove expired bags by shifting remaining elements.
  for (int i = 0; i < bloodBagCount; ) {
    unsigned long age = (currentTime - bloodBags[i].storedTime) / 1000; // age in seconds
    if (age >= SHELF_LIFE) {
      Serial.println("Removing expired bag: " + bloodBags[i].id);
      // Shift remaining items left
      for (int j = i; j < bloodBagCount - 1; j++) {
        bloodBags[j] = bloodBags[j + 1];
      }
      bloodBagCount--;
      removedCount++;
      // Do not increment i because new element occupies current index
    } else {
      i++;
    }
  }
  Serial.println("Expired bags removed: " + String(removedCount));
}

// Function to count expired blood bags (without removing)
int countExpiredBags() {
  int expiredCount = 0;
  unsigned long currentTime = millis();
  for (int i = 0; i < bloodBagCount; i++) {
    unsigned long age = (currentTime - bloodBags[i].storedTime) / 1000;
    if (age >= SHELF_LIFE) {
      expiredCount++;
    }
  }
  return expiredCount;
}

void setup() {
  Serial.begin(115200);
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while(WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");

  // Initialize ThingSpeak
  ThingSpeak.begin(client);
  
  // Initialize DHT22 sensor
  dhtSensor.setup(DHT_PIN, DHTesp::DHT22);
  
  // Initialize LCD display
  lcd.init();
  lcd.backlight();
  
  // Initialize buzzer
  pinMode(BUZZER_PIN, OUTPUT);
  
  // Initialize buttons (active LOW)
  pinMode(BUTTON_ADD, INPUT_PULLUP);
  pinMode(BUTTON_REMOVE, INPUT_PULLUP);
  
  // Display welcome message
  lcd.setCursor(0, 0);
  lcd.print("Blood Bank IoT");
  lcd.setCursor(0, 1);
  lcd.print("Monitoring...");
  delay(2000);
  lcd.clear();
  
  lastThingSpeakUpdate = millis();
}

void loop() {
  // Check if the "add blood bag" button is pressed
  if (digitalRead(BUTTON_ADD) == LOW) {
    addBloodBag("Bag" + String(bloodBagCount + 1));
    delay(200); // debounce delay
  }
  
  // Check if the "remove expired bags" button is pressed
  if (digitalRead(BUTTON_REMOVE) == LOW) {
    removeExpiredBags();
    delay(500); // debounce delay
  }
  
  // Read sensor data every 2 seconds
  TempAndHumidity data = dhtSensor.getTempAndHumidity();
  if (isnan(data.temperature) || isnan(data.humidity)) {
    Serial.println("Sensor read error!");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Sensor Error!");
    delay(2000);
    return;
  }
  
  // Accumulate sensor readings for averaging
  temperatureSum += data.temperature;
  humiditySum += data.humidity;
  sampleCount++;
  
  // Display current sensor reading on LCD
  String tempStr = "Temp: " + String(data.temperature, 2) + " C";
  String humStr  = "Hum: " + String(data.humidity, 1) + " %";
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(tempStr);
  lcd.setCursor(0, 1);
  lcd.print(humStr);
  
  // Log sensor readings and inventory info to Serial Monitor
  Serial.println(tempStr);
  Serial.println(humStr);
  Serial.println("Total bags: " + String(bloodBagCount));
  Serial.println("Expired bags: " + String(countExpiredBags()));
  
  // Check for alerts (if environmental values are out-of-range)
  bool alert = false;
  if (data.temperature < TEMP_LOW || data.temperature > TEMP_HIGH) {
    Serial.println("ALERT: Temperature out of safe range!");
    alert = true;
  }
  if (data.humidity < HUMID_LOW || data.humidity > HUMID_HIGH) {
    Serial.println("ALERT: Humidity out of safe range!");
    alert = true;
  }
  
  if (alert) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("!! ALERT !!");
    lcd.setCursor(0, 1);
    lcd.print("Check Env.");
    tone(BUZZER_PIN, 1000, 500);
  } else {
    noTone(BUZZER_PIN);
  }
  
  Serial.println("---");
  
  // Every 15 seconds, compute averages and send data to ThingSpeak
  if (millis() - lastThingSpeakUpdate >= 15000) {
    float avgTemperature = temperatureSum / sampleCount;
    float avgHumidity    = humiditySum / sampleCount;
    
    int totalBags = bloodBagCount;
    int expiredBags = countExpiredBags();
    
    ThingSpeak.setField(1, avgTemperature);
    ThingSpeak.setField(2, avgHumidity);
    ThingSpeak.setField(3, totalBags);
    ThingSpeak.setField(4, expiredBags);
    
    int responseCode = ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey);
    if (responseCode == 200) {
      Serial.println("Data sent to ThingSpeak successfully.");
    } else {
      Serial.println("Problem sending data. HTTP error code " + String(responseCode));
    }
    
    // Reset accumulators for the next 15-second period
    temperatureSum = 0;
    humiditySum = 0;
    sampleCount = 0;
    lastThingSpeakUpdate = millis();
  }
  
  delay(2000); // 2-second interval for sensor reading and display update
}
