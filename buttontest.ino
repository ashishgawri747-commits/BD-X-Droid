#define BTN_PIN 22  

void setup() {
  pinMode(BTN_PIN, OUTPUT);
  digitalWrite(BTN_PIN, LOW); 
  delay(2000);                 
  digitalWrite(BTN_PIN, HIGH); 
  delay(5000);                 
  digitalWrite(BTN_PIN, LOW);  
}

void loop() {
}
