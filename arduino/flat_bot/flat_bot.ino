#include <Stepper.h>

#define LIMIT1 (!digitalRead(A0))
#define LIMIT2 (!digitalRead(A1))

#define STEPS_PER_REV 2048 // Steps per revolution for this motor
#define SPEED 12

#define STEPSIZE 1

Stepper stepper1(STEPS_PER_REV, 8, 10, 9, 11);
Stepper stepper2(STEPS_PER_REV, 4, 5, 3, 6);

int stepperPos1 = 0;
int stepperPos2 = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("Ready");
  stepper1.setSpeed(SPEED);
  stepper2.setSpeed(SPEED);
  stepperGo1(-1000);
  stepperGo2(-1000);
}

void stepperGo1(int moveToDeg) {
  long stepsToTake = (moveToDeg / 360.0) * STEPS_PER_REV - stepperPos1;
  Serial.print("stepper1 stepsToTake: ");
  Serial.println(stepsToTake);

  // Forward
  if (stepsToTake > 0) {
    Serial.println("Forward");
    for (int i = 1; i <= abs(stepsToTake); i += STEPSIZE) {
      stepper1.step(STEPSIZE);
      stepperPos1 += STEPSIZE;
    }
  }

  // Reverse
  if (stepsToTake < 0) {
    Serial.println("Reverse");
    for (int i = 1; i <= abs(stepsToTake); i += STEPSIZE) {
      if (LIMIT1) {
        Serial.println("Hit LIMIT1");
        stepperPos1 = 0;
        break;
      }
      stepper1.step(-STEPSIZE);
      stepperPos1 -= STEPSIZE;
    }
  }

  Serial.print("stepperPos1: ");
  Serial.println(stepperPos1);
}

void stepperGo2(int moveToDeg) {
  long stepsToTake = (moveToDeg / 360.0) * STEPS_PER_REV - stepperPos2;
  Serial.print("stepper2 stepsToTake: ");
  Serial.println(stepsToTake);

  // Forward
  if (stepsToTake > 0) {
    Serial.println("Forward");
    for (int i = 1; i <= abs(stepsToTake); i += STEPSIZE) {
      stepper2.step(-STEPSIZE); // This is flipped for stepper 2
      stepperPos2 += STEPSIZE;
    }
  }

  // Reverse
  if (stepsToTake < 0) {
    Serial.println("Reverse");
    for (int i = 1; i <= abs(stepsToTake); i += STEPSIZE) {
      if (LIMIT2) {
        Serial.println("Hit LIMIT2");
        stepperPos2 = 0;
        break;
      }
      stepper2.step(STEPSIZE); // This is flipped for stepper 2
      stepperPos2 -= STEPSIZE;
    }
  }

  Serial.print("stepperPos2: ");
  Serial.println(stepperPos2);
}

void checkSerial() {
  if (Serial.available()) {
    switch (Serial.read()) {
      case 'h':
        Serial.println("hello");
        break;
      case 's':
        Serial.print(LIMIT1);
        Serial.print(" ");
        Serial.println(LIMIT2);
        break;
      case '0':
        Serial.println('0');
        stepperGo1(-1000);
        break;
      case '1':
        Serial.println('1');
        stepperGo1(10);
        break;
      case '2':
        Serial.println('2');
        stepperGo1(20);
        break;
      case '3':
        Serial.println('3');
        stepperGo1(30);
        break;
      case '4':
        Serial.println('4');
        stepperGo1(40);
        break;
      case ')':
        Serial.println('0');
        stepperGo2(-1000);
        break;
      case '!':
        Serial.println('1');
        stepperGo2(10);
        break;
      case '@':
        Serial.println('2');
        stepperGo2(20);
        break;
      case '#':
        Serial.println('3');
        stepperGo2(30);
        break;
      case '$':
        Serial.println('4');
        stepperGo2(40);
        break;
    }
  }
}

void loop() {
  checkSerial();
  delay(500);
}
