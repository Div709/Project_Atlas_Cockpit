#include <Wire.h>
#include <LiquidCrystal_PCF8574.h>

// ==================================
// LCD
// ==================================

LiquidCrystal_PCF8574 lcd(0x27);

// ==================================
// PIN DEFINITIONS
// ==================================

#define POT_PIN     34
#define BUTTON_PIN  25

#define MOTOR_PWM   23
#define MOTOR_IN1   19
#define MOTOR_IN2   18

// ==================================
// ENGINE VARIABLES
// ==================================

String engineState = "OFF";

unsigned long startTime = 0;

int lastButtonState = HIGH;

// ==================================
// MPU6500 VARIABLES
// ==================================

int16_t ax = 0;
int16_t ay = 0;
int16_t az = 0;

// ==================================
// READ MPU6500
// ==================================

void readMPU()
{
    Wire.beginTransmission(0x68);

    Wire.write(0x3B);

    Wire.endTransmission(false);

    Wire.requestFrom(0x68, 6);

    if (Wire.available() == 6)
    {
        ax = (Wire.read() << 8) | Wire.read();
        ay = (Wire.read() << 8) | Wire.read();
        az = (Wire.read() << 8) | Wire.read();
    }
}

// ==================================
// SETUP
// ==================================

void setup()
{
    Serial.begin(115200);

    // I2C
    Wire.begin(21, 22);

    // Wake MPU6500
    Wire.beginTransmission(0x68);
    Wire.write(0x6B);
    Wire.write(0x00);
    Wire.endTransmission();

    // Button
    pinMode(BUTTON_PIN, INPUT_PULLUP);

    // Motor pins
    pinMode(MOTOR_PWM, OUTPUT);
    pinMode(MOTOR_IN1, OUTPUT);
    pinMode(MOTOR_IN2, OUTPUT);

    // Motor direction
    digitalWrite(MOTOR_IN1, HIGH);
    digitalWrite(MOTOR_IN2, LOW);

    // LCD
    lcd.begin(16, 2);
    lcd.setBacklight(255);

    lcd.setCursor(0, 0);
    lcd.print("ATLAS V2");

    lcd.setCursor(0, 1);
    lcd.print("BOOTING...");

    delay(1500);

    lcd.clear();
}

// ==================================
// MAIN LOOP
// ==================================

void loop()
{
    // ------------------------------
    // Read Inputs
    // ------------------------------

    int potValue = analogRead(POT_PIN);

    int buttonState = digitalRead(BUTTON_PIN);

    // ------------------------------
    // Read MPU6500
    // ------------------------------

    readMPU();

    // ------------------------------
    // Button Edge Detection
    // ------------------------------

    if (buttonState == LOW &&
        lastButtonState == HIGH)
    {
        if (engineState == "OFF")
        {
            engineState = "STARTING";

            startTime = millis();
        }
        else if (engineState == "RUNNING")
        {
            engineState = "SHUTTING OFF";

            startTime = millis();
        }
    }

    lastButtonState = buttonState;

    // ------------------------------
    // Startup Timer
    // ------------------------------

    if (engineState == "STARTING" &&
        millis() - startTime > 2000)
    {
        engineState = "RUNNING";
    }

    // ------------------------------
    // Shutdown Timer
    // ------------------------------

    if (engineState == "SHUTTING OFF" &&
        millis() - startTime > 2000)
    {
        engineState = "OFF";
    }

    // ------------------------------
    // RPM Calculation
    // ------------------------------

    int rpm = 0;

    if (engineState == "RUNNING")
    {
        rpm = map(
            potValue,
            0,
            4095,
            0,
            5000
        );
    }

    // ------------------------------
    // Motor Speed Control
    // ------------------------------

    int motorSpeed = map(
        rpm,
        0,
        5000,
        0,
        255
    );

    analogWrite(MOTOR_PWM, motorSpeed);

    // ------------------------------
    // Serial Telemetry
    // ------------------------------

    Serial.print("POT=");
    Serial.print(potValue);

    Serial.print(",STATE=");
    Serial.print(engineState);

    Serial.print(",RPM=");
    Serial.print(rpm);

    Serial.print(",AX=");
    Serial.print(ax);

    Serial.print(",AY=");
    Serial.print(ay);

    Serial.print(",AZ=");
    Serial.println(az);

    // ------------------------------
    // LCD Line 1
    // ------------------------------

    lcd.setCursor(0, 0);

    lcd.print("RPM:");
    lcd.print(rpm);
    lcd.print("     ");

    // ------------------------------
    // LCD Line 2
    // ------------------------------

    lcd.setCursor(0, 1);

    if (engineState == "OFF")
    {
        lcd.print("ENGINE OFF     ");
    }
    else if (engineState == "STARTING")
    {
        lcd.print("STARTING...    ");
    }
    else if (engineState == "SHUTTING OFF")
    {
        lcd.print("SHUTTING OFF.. ");
    }
    else if (engineState == "RUNNING")
    {
        lcd.print("ENGINE RUNNING ");
    }

    delay(10);
}