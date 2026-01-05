#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
Adafruit_MPU6050 mpu;
void setup() {
  Serial.begin(9600);
  Wire.begin();
  if (!mpu.begin()) {
   Serial.println("MPU6050 not found!");
   while (1);
   }
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
}
 
void position(){
 sensors_event_t accel, gyro, temp;
 mpu.getEvent(&accel, &gyro, &temp);
 float pitch=atan2(accel.acceleration.y, accel.acceleration.z) * 180/PI;
 float roll=atan2(-accel.acceleration.x,sqrt(accel.acceleration.y*accel.acceleration.y + accel.acceleration.z*accel.acceleration.z))*180/PI;
 Serial.print("Pitch:");
 Serial.print(pitch);
 Serial.print("roll:");
 Serial.println(roll);
 delay(1000); 
}

void loop(){
}

      
    
