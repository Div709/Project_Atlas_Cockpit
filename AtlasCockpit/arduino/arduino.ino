#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

String engineState = "OFF";

unsigned long startTime = 0;

int lastButtonState = 1;

void setup()
{
    Serial.begin(9600);

    pinMode(2, INPUT);
    pinMode(5, OUTPUT);
    pinMode(7, OUTPUT);
    pinMode(8, OUTPUT);

    digitalWrite(7, HIGH);
    digitalWrite(8, LOW);

    lcd.init();
    lcd.backlight();

    lcd.setCursor(0, 0);
    lcd.print("ATLAS COCKPIT");

    delay(1000);

    lcd.clear();
}

void loop()
{
    int potValue = analogRead(A0);
    int buttonState = digitalRead(2);


    // Detect button press

    if (
        buttonState == 0 &&
        lastButtonState == 1 &&
        engineState == "OFF"
    )
    {
        engineState = "STARTING";
        startTime = millis();
    }

    lastButtonState = buttonState;

    // Engine startup timing

    if (
        engineState == "STARTING" &&
        millis() - startTime > 2000
    )
    {
        engineState = "RUNNING";
    }

    // RPM calculation

    int rpm = 0;

    if (engineState == "RUNNING")
    {
        rpm = map(potValue, 0, 1023, 0, 5000);
    }
    int motorSpeed = map(rpm, 0, 5000, 0, 255);
    analogWrite(5, motorSpeed);

    // Send telemetry to Python

    Serial.print("POT=");
    Serial.print(potValue);

    Serial.print(",STATE=");
    Serial.print(engineState);

    Serial.print(",RPM=");
    Serial.println(rpm);

    // LCD Line 1

    lcd.setCursor(0, 0);
    lcd.print("RPM:");
    lcd.print(rpm);
    lcd.print("        ");

    // LCD Line 2

    lcd.setCursor(0, 1);

    if (engineState == "OFF")
    {
        lcd.print("ENGINE OFF     ");
    }
    else if (engineState == "STARTING")
    {
        lcd.print("STARTING...    ");
    }
    else
    {
        lcd.print("ENGINE RUNNING ");
    }

    delay(20);
}