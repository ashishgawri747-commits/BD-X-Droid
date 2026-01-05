#include <Servo.h>
Servo servo1;
Servo servo2;
int servo1Pin = 9;
int servo2Pin = 10;


void setup() {
  Serial1.begin(9600);  
  servo1.attach(servo1Pin);
  servo2.attach(servo2Pin);
  Serial1.println("Arduino ready");
}

void loop() {
  if (Serial1.available()) {
    String cmd = Serial1.readStringUntil('\n');
    cmd.trim();

    if (cmd.startsWith("S1:")) {
      int angle = cmd.substring(3).toInt();
      servo1.write(angle);
      Serial1.print("Servo1 moved to ");
      Serial1.println(angle);
    }
    else if (cmd.startsWith("S2:")) {
      int angle = cmd.substring(3).toInt();
      servo2.write(angle);
      Serial1.print("Servo2 moved to ");
      Serial1.println(angle);
    }
  }
}
