#include <Servo.h>
Servo rtop;
Servo rmid;
Servo ltop;
Servo lmid;
void move_slow(Servo &s, int from, int to, int stepDelay){
  if (from<to){
    for (int p=from; p<= to; p++){
      delay(30);
      s.write(p);
      delay(stepDelay);
    }
    }else{
      for(int p= from; p>= to; p--){
        delay(30);
        s.write(p);
        delay(stepDelay);
      }
    }
  }
void setup(){
  rtop.attach(7);
  rmid.attach(8);
  ltop.attach(9);
  lmid.attach(10);
  rtop.write(90);
  rmid.write(90);
  lmid.write(90);
  ltop.write(90);
  move_slow(lmid,120,130,20);
  move_slow(ltop,90,50,10);
  move_slow(lmid,70,65,20);
  move_slow(rmid,90-20,90-20,20);
  move_slow(rtop,90,90+20,20);
}


void loop(){
  
}
