#include "DHT.h"
#include <DS3231.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);     // you need to know I2C address of your LCD, library will help you
DS3231  rtc(SDA, SCL);                  // you need to set current time on RTC, again, library will help
DHT dht(7, DHT22);
Time  t;

#define Hum 3         // Humidifier relay pin
#define Fan 4         // Fan relay pin
#define LED 5         // Led relay pin

bool backlightFlag = 1, fanSleep = 0;                      // flags
long fanSleepingTime = 1800000;                            // default fan sleeping time: 30 minutes
unsigned long fanSleepTimer = 0, sensTimer = 0;            // timers
long sensorUpdate = 5000;                                  // how often to read sensors (must be 2+ sec)

byte hour, min;         // to store data from RTC
byte LedOn, LedOff;     // When to turn on/off the lights

byte temp, hum;                     // store data from DHT sensor
byte minTemp = 20, maxTemp = 26;    // climate levels, which can
byte minHum = 40, maxHum = 80;      // be changed in bot menu

String command;       // Variables for serial control and parse
char input;
char setter[] = "";
int setterVal;


void setup() {
  Serial.begin(115200);
  Serial.println("I am ready!");
  pinMode(Fan, OUTPUT);
  dht.begin();
  rtc.begin();
  lcd.init();
  lcd.backlight();
  lcd.clear();
  readSensors();
}

void readSensors() {
  hum = dht.readHumidity();
  delay(50);
  temp = dht.readTemperature();
  t = rtc.getTime();
  hour = (t.hour);
  min = (t.min);
}

void lightingControl() {
  if ( (hour >= LedOn) && (hour < LedOff) ) {     // need to re-write this logic, because it woun't work properly in night time
    digitalWrite(LED, HIGH);
  }
  else {
    digitalWrite(LED, LOW);
  }
}

void climateControl() {
  if (fanSleep != 1) {
    if (temp <= minTemp) {      // if temp falls, fan will not work to allow the lights to heat up the tent
      digitalWrite(Fan, LOW);   // need to re-write this for night time, when lights are off and temp is low
    }
    else {
      digitalWrite(Fan, HIGH);  // ideally, fan should be working all the time
    }
  }
  else {                        // sleeping mode
    digitalWrite(Fan, LOW);
    if (millis() - fanSleepTimer > fanSleepingTime) {
      fanSleep = 0;
    }
  }

  if (hum >= maxHum) {          // humidifier control
    digitalWrite(Hum, LOW);
  }
  else if (hum <= minHum) {
    digitalWrite(Hum, HIGH);
  }
}

void lcdUpdate() {
  lcd.clear();
  lcd.setCursor(0, 0);    // write temp and hum to LCD's first line
  lcd.print("Temp:");
  lcd.print(temp);
  lcd.print(char(223));
  lcd.print(" ");
  lcd.print("Hum:");
  lcd.print(hum);
  lcd.print("%");
  lcd.setCursor(0,1);     // write RTC time to LCD's second line
  lcd.print(hour);
  lcd.print(":");
  lcd.print(min);
  lcd.print("  ");
}

//----------------------- MAIN LOOP ------------------------
void loop() {
  if (Serial.available() > 0) {       // if there is any text in serial, parse it
    input = Serial.read();
    if (input != '\n') {
      command += input;
    }
    else {
      serialControl();
    }
  }

  if (millis() - sensTimer > sensorUpdate) {        // if sensor update time has passed - do main routine
    sensTimer = millis();     // nullify the update timer
    readSensors();            // get info from sensors
    lcdUpdate();              // show info on LCD
    climateControl();         // control Fan and Humidifier
    lightingControl();        // Switch on/off lights
  }
}

//------------------------ Control over serial ------------------------
void serialControl() {
  if (command.equalsIgnoreCase("info")) {
    Serial.print(temp);
    Serial.print(";");
    Serial.println(hum);
  }
  else if (command.equalsIgnoreCase("led on")) {
    digitalWrite(LED, HIGH);
    Serial.println("Lights are turned on.");
  }
  else if (command.equalsIgnoreCase("led off")) {
    digitalWrite(LED, LOW);
    Serial.println("Lights are turned off.");
  }
  else if (command.equalsIgnoreCase("fan on")) {
    digitalWrite(Fan, HIGH);
    fanSleep = 0;
    sensTimer = millis();
    Serial.println("Fan is working in usual mode.");
  }
  else if (command.equalsIgnoreCase("fan off")) {
    digitalWrite(Fan, LOW);
    fanSleep = 0;
    sensTimer = millis();
    Serial.println("The fan is turned off.");
  }
  else if (command.equalsIgnoreCase("fan sleep")) {
    digitalWrite(Fan, LOW);
    fanSleep = 1;
    fanSleepTimer = millis();
    Serial.println("Putting fan into sleep mode for 1 hour");
  }
  else if (command.equalsIgnoreCase("backlight")) {
    if (backlightFlag == 1) {
      lcd.noBacklight();
      backlightFlag = 0;
      Serial.println("LCD backlight turned off.");
    }
    else {
      lcd.backlight();
      backlightFlag = 1;
      Serial.println("LCD backlight turned on.");
    }
  }
  else if (command.equalsIgnoreCase("get sensor")) {
    Serial.print("Sensors update every: ");
    Serial.print(sensorUpdate / 1000);
    Serial.println(" seconds");
  }
  else if (command.equalsIgnoreCase("get fan sleep")) {
    Serial.print("Fan sleep time: ");
    Serial.print(fanSleepingTime / 1000 / 60);
    Serial.println(" minutes");
  }
  else if (command.equalsIgnoreCase("get climate")) {
    Serial.print("Min temp is: ");
    Serial.print(minTemp);
    Serial.print(" max temp is: ");
    Serial.print(maxTemp);
    Serial.print(" | Min hum is: ");
    Serial.print(minHum);
    Serial.print('%');
    Serial.print(" max hum is: ");
    Serial.print(maxHum);
    Serial.println('%');
  }
  else if (command.equalsIgnoreCase("get schedule")) {
    Serial.print("Current lighting schedule is");
    Serial.print(LedOn);
    Serial.print(":00-");
    Serial.print(LedOff);
    Serial.println(":00");
  }

  else if (command.indexOf(':') > 4) {
    serialParse();
  }
  else {
  }
  command = "";
}
//------------------------- Serial command parse --------------------------
void serialParse() {
  char buff[20];
  command.toCharArray(buff, 20);
  char* strtokIndx;
  strtokIndx = strtok(buff, ":");
  strcpy(setter, strtokIndx);
  String setterStr(setter);
  strtokIndx = strtok(NULL, ":");
  setterVal = atoi(strtokIndx);

  if (setterStr.equalsIgnoreCase("ledon")) {
    if ((setterVal < 25) && (setterVal > -1)) {
      LedOn = setterVal;
      Serial.print("Lights will turn on at ");
      Serial.print(LedOn);
      Serial.println(":00");
    }
    else {
      Serial.println("Incorrect value, please choose between 0-24");
    }
  }
  else if (setterStr.equalsIgnoreCase("ledoff")) {
    if ((setterVal < 25) && (setterVal > -1)) {
      LedOff = setterVal;
      Serial.print("Lights will turn off at ");
      Serial.print(LedOff);
      Serial.println(":00");

    }
    else {
      Serial.println("Incorrect value, please choose between 0-24");
    }
  }

  else if (setterStr.equalsIgnoreCase("maxhum")) {
    if (setterVal < 101) {
      maxHum = setterVal;
      Serial.print("Max humidity level updated: ");
      Serial.print(maxHum);
      Serial.println("%");
    }
    else {
      Serial.println("Incorrect humidity, please choose between 0-100%");
    }
  }
  else if (setterStr.equalsIgnoreCase("minhum")) {
    if (setterVal < 101) {
      minHum = setterVal;
      Serial.print("Min humidity level updated: ");
      Serial.print(minHum);
      Serial.println("%");
    }
    else {
      Serial.println("Incorrect humidity, please choose between 0-100%");
    }
  }

  else if (setterStr.equalsIgnoreCase("maxtemp")) {
    if ((setterVal < 80) && (setterVal > -40)) {
      maxTemp = setterVal;
      Serial.print("Max temp level updated: ");
      Serial.println(maxTemp);
    }
    else {
      Serial.println("Incorrect temperature, please choose between -40 and +80");
    }
  }
  else if ( (setterStr.equalsIgnoreCase("mintemp")) && (setterVal < 50) ) {
    if ((setterVal < 80) && (setterVal > -40)) {
      minTemp = setterVal;
      Serial.print("Min temp level updated: ");
      Serial.println(minTemp);
    }
    else {
      Serial.println("Incorrect temperature, please choose between -40 and +80");
    }
  }

  else if (setterStr.equalsIgnoreCase("set sensor")) {
    if ( (setterVal < 86400000) && (setterVal > 2) ) {
      sensorUpdate = setterVal*1000L;                         // 'L' to force the constant into a long data format
      Serial.print("Sensors update every: ");
      Serial.print(sensorUpdate / 1000);
      Serial.println(" seconds");
    }
    else {
      Serial.println("Please choose another value");
    }
  }

}
