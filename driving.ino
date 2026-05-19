const int motorPinR1 = 7;
const int motorPinR2 = 8;
const int motorPinREna = 6;

const int motorPinL1 = 9;
const int motorPinL2 = 10;
const int motorPinLEna = 11;

void moveMotor(int motorPin1, int motorPin2, int motorPinEna, int direction, int speed) {
  if (direction == 1){
    digitalWrite(motorPin1, HIGH);
    digitalWrite(motorPin2, LOW);
  }
  else if (direction == -1) {
    digitalWrite(motorPin1, LOW);
    digitalWrite(motorPin2, HIGH);
  }
  else {
    digitalWrite(motorPin1, LOW);
    digitalWrite(motorPin2, LOW);
  }
  analogWrite(motorPinEna, speed);
}

void moveForward(int speed) {
  moveMotor(motorPinR1, motorPinR2, motorPinREna, 1, speed);
  moveMotor(motorPinL1, motorPinL2, motorPinLEna, 1, speed);
}

void moveBackward(int speed) {
  moveMotor(motorPinR1, motorPinR2, motorPinREna, -1, speed);
  moveMotor(motorPinL1, motorPinL2, motorPinLEna, -1, speed);
}

void rightMotor(int speed) {
  moveMotor(motorPinR1, motorPinR2, motorPinREna, 1, speed);
  moveMotor(motorPinL1, motorPinL2, motorPinLEna, -1, speed);
}

void leftMotor(int speed) {
  moveMotor(motorPinR1, motorPinR2, motorPinREna, -1, speed);
  moveMotor(motorPinL1, motorPinL2, motorPinLEna, 1, speed);
}

void stopMotors() { HIGH);
    digitalWrite(motorPin2, LOW);
  }                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
  moveMotor(motorPinR1, motorPinR2, motorPinREna, 0, 0);
  moveMotor(motorPinL1, motorPinL2, motorPinLEna, 0, 0);
}
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(motorPinR1, OUTPUT);
  pinMode(motorPinR2, OUTPUT);
  pinMode(motorPinREna, OUTPUT);
  
  pinMode(motorPinL1, OUTPUT);
  pinMode(motorPinL2, OUTPUT);
  pinMode(motorPinLEna, OUTPUT);
}

void loop() {
  if(Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    whspeed = int(data)
    Serial.print(data);
    if(-20<whspeed<20){
      moveForward(100);
    }
    else if(0<whspeed<160){
      rightMotor(whspeed);
      leftMotor(whspeed - 159);
    }
    else if(0>whspeed>-160){
      rightMotor(whspeed-159);
      leftMotor((whspeed*-1)-159);
    }

    
  }
