#include <Servo.h>

int pos = 5;
int pos1 = 5;
Servo servo_8;
Servo servo_9;

void setup() {
    Serial.begin(9600);
    servo_8.attach(8, 500, 2500);
    servo_9.attach(9, 500, 2500);
  }
  
void loop() {
    if (Serial.available() > 0) {
      int signal = Serial.parseInt();  // read integer sent from Python
      if (signal == 1) { // Biodegradable
        for(pos1 = 5; pos1 <= 150; pos1++) {
            servo_8.write(pos1);
            delay(20);
        }


        for(pos1 = 5; pos1 <= 150; pos1--) {
            servo_8.write(pos1);
            delay(20);
        }

        delay(500);
      } else if (signal == 2) { // Non-Biodegradable
        for(pos = 5; pos <= 140; pos++) {
            servo_9.write(pos);
            delay(20);
        }

        for(pos = 5; pos <= 140; pos--) {
            servo_9.write(pos);
            delay(20);
        }

        delay(700);
      }
    }
  }