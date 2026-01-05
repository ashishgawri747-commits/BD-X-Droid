#include <Servo.h>
Servo base;
Servo mid;
Servo pan;
void setup(){
  base.attach(9);
  mid.attach(10);
  pan.attach(11);
  pan.write(90);
  delay(500);
  mid.write(120);
  delay(500);
  base.write(180);
}
void loop(){
  
}
