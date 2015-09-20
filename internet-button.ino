#include "InternetButton/InternetButton.h"


InternetButton b = InternetButton();
bool urgent_mode = false;

void setup()
{
    b.begin();

    Spark.function("led", led);
}

void loop()
{
   if (b.allButtonsOn()) {
       if (urgent_mode == true) {
           urgent_mode = false;
           b.playNote("G5", 8);
           b.allLedsOn(255, 0, 0);
           delay(500);
           b.allLedsOff();
       }
   } else if (urgent_mode == true) {
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
    if (command == "urgent") {
        urgent_mode = true;
        b.playSong("E5,8,G5,8,E6,8,C6,8,D6,8,G6,8");
        return 1;
    }
    else if (command == "off") {
        urgent_mode = false;
        b.allLedsOff();
        return 0;
    }
    return -1;
}

