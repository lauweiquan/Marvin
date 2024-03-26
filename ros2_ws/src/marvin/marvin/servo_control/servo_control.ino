#include <Servo.h>

Servo servo[3];
int default_angle[3] = {60, 60, 60};

void setup()
{
    Serial.begin(9600);
    // Serial.println("serial began");
    servo[0].attach(5);
    servo[1].attach(6);
    servo[2].attach(7);

    for (size_t i = 0; i < 3; i++)
    {
        servo[i].write(default_angle[i]);
    }
}

byte angle[6];
byte pre_angle[3];
long t = millis();
const float Pi = 3.141593;

void loop()
{
    Serial.write("testing");
    // Serial.print("looping");
    if (Serial.available())
    // Serial.println("serial is avail");
    {
        Serial.readBytes(angle, 6);
        for (size_t i = 0; i < 3; i++)
        {
            angle[i] = angle[i] * (180/Pi);
            Serial.print(angle[i]);
            if (angle[i] != pre_angle[i])
            {
                servo[i].write(angle[i]);
                pre_angle[i] = angle[i];
            }
        }
        t = millis();
    }

    if (millis() - t > 1000)
    {
        for (size_t i = 0; i < 3; i++)
        {
            servo[i].write(default_angle[i]);
            pre_angle[i] = default_angle[i];
        }
    }
}
