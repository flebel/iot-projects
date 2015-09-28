#include "InternetButton/InternetButton.h"


InternetButton b = InternetButton();
bool urgentMode = false;

void setup()
{
    b.begin();

    Spark.function("led", led);
    Spark.function("leds_upto", ledsUpto);
}

void loop()
{
   if (b.allButtonsOn()) {
       if (urgentMode == true) {
           urgentMode = false;
           b.playNote("G5", 8);
           b.allLedsOn(255, 0, 0);
           delay(500);
           b.allLedsOff();
       }
   } else if (urgentMode == true) {
        for (int led = 1; led < 12; led++) {
            b.ledOff(led - 1);
            b.ledOn(led, 0, 255, 0);
            delay(50);
            b.ledOn(led - 1, 255, 0, 0);
            b.ledOn(led, 0, 255, 0);
            delay(50);
            b.ledOff(led);
        }
        b.allLedsOff();
        delay(1500);
   }
}

int led(String command) {
    Spark.publish("Command '" + command + "' called.", NULL, 60, PRIVATE);
    if (command == "off") {
        urgentMode = false;
        b.allLedsOff();
        return 0;
    } else if (command == "urgent") {
        urgentMode = true;
        b.playSong("E5,8,G5,8,E6,8,C6,8,D6,8,G6,8");
        return 1;
    }
    return -1;
}

int ledsUpto(String ledNumber) {
    b.allLedsOff();
    int maxNumberLoops = 3;
    for (int led = 0, leds = ledNumber.toInt(), loops = 0; led < leds && loops <= maxNumberLoops; led++) {
        if (led < 4) {
            b.ledOn(led, 0, 255, 0);
        } else if (led < 7) {
            b.ledOn(led, 255, 255, 0);
        } else if (led < 9) {
            b.ledOn(led, 255, 165, 0);
        } else {
            b.ledOn(led, 255, 0, 0);
        }
        delay(75);
        if (led == (leds - 1) && leds > 7) {
            if (loops < maxNumberLoops) {
                b.allLedsOff();
            }
            led = 0;
            loops++;
            delay(250);
        }
    }
    return 1;
}

