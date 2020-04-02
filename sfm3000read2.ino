#include <Wire.h>

long t = 0;
float gas = 140.0;

int resetSensor(){
  Wire.beginTransmission(0x40);
  Wire.write(0x20);
  Wire.write(0x00);
  int et = Wire.endTransmission();
  return et;
}

int continuousMode(){
  Wire.beginTransmission(0x40);
  Wire.write(0x10);
  Wire.write(0x00);
  Wire.endTransmission();
  int et = Wire.endTransmission();
  return et;
}

void setup() {
  // put your setup code here, to run once:
  Wire.begin();
  Serial.begin(9600);

  resetSensor();
  delay(300);
  continuousMode();
  delay(200);

  
}



float pollflowsensor() {
  uint16_t raw;
  float slm = 0;
  int16_t value;

  // put your main code here, to run repeatedly:
  Wire.requestFrom(0x40, 3);
  if (Wire.available() < 3) {
    Serial.println("ER");
    slm = 0;
  } else {

    //Three bytes available, the first two are a 16 bit measurement
    //The last is a CRC of that measurement
    //We ignore the latter
    raw = Wire.read() << 8;
    raw |= Wire.read();
    //uint16_t raw_crc = Wire.read();

    value = (int16_t) raw;
    slm = ( value - 32000 ) / gas;
  }
  return slm;
}

uint32_t serialNumber(){
  Wire.beginTransmission(0x40);
  Wire.write(0x31);
  Wire.write(0xAE);
  Wire.endTransmission();
  int et = Wire.endTransmission();

  uint32_t result = 0;

  Wire.requestFrom(0x40, 3);
  if (Wire.available() < 4) {
       Serial.print("SNbytesavail=");
       Serial.print(Wire.available());
       uint32_t raw;
       raw = Wire.read() << 8;
       raw |= Wire.read() << 8;
       raw |= Wire.read() << 8;
       raw |= Wire.read() << 8;

       result = raw ;
  }
  else
  {
     result=et;
  }
  
  return result;
}

void loop() {
  int cmd;

  if (Serial.available() > 0) {
    
    cmd = Serial.read();
    //Serial.println(cmd);
    // cmd = 'd'   -- return data
    if (cmd == 100) {
      Serial.println(pollflowsensor());
    }
    // cmd = '?'   -- return help
    if (cmd == 63) {
      Serial.println("help=d,?,s,c,r,a,o");
    }
    // cmd = 's'   -- return serial number
    if (cmd == 115) {
      Serial.println(serialNumber());
    }
    // cmd = 'r'   -- soft reset
    if (cmd == 114) {
      Serial.println(resetSensor());
    }    
    // cmd = 'c'   -- continuous mode
    if (cmd == 99) {
      Serial.println(continuousMode());
    }
    // cmd = 'a'   -- air
    if (cmd == 97) {
      gas = 140.0;
      Serial.println('air');
    }
    // cmd = 'o'   -- oxygen
    if (cmd == 111) {
      gas = 142.8;
      Serial.println('oxygen');
    }
  }

}
