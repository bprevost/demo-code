#include <IRremote.h>

// For IR remote
#define IR_KEY_FORWARD 16736925
#define IR_KEY_BACK 16754775
#define IR_KEY_LEFT 16720605
#define IR_KEY_RIGHT 16761405
#define IR_KEY_STOP 16712445

// For IR remote
#define IR_PIN 12
IRrecv ir_receiver(IR_PIN);
decode_results ir_results;

// For motors (L293D chip)
#define MOTOR_ENA_PIN 5 // Green
#define MOTOR_IN1_PIN 7 // Yellow
#define MOTOR_IN2_PIN 8 // Orange
#define MOTOR_ENB_PIN 6 // Green
#define MOTOR_IN3_PIN 9 // Yellow
#define MOTOR_IN4_PIN 11 // Orange

const int move_speed = 255; // [0, 255]
const int turn_speed = 255; // [0, 255]

enum STATE {
  STOP,
  FORWARD,
  BACK,
  LEFT,
  RIGHT,
} state = STOP;

void setup() {
  // Put setup code here, to run once:

  // For serial communications
  Serial.begin(9600);
  Serial.println("Begin");

  // For IR remote
  ir_receiver.enableIRIn();

  // For motors (L293D chip)
  pinMode(MOTOR_IN1_PIN, OUTPUT);
  pinMode(MOTOR_IN2_PIN, OUTPUT);
  pinMode(MOTOR_IN3_PIN, OUTPUT);
  pinMode(MOTOR_IN4_PIN, OUTPUT);
  pinMode(MOTOR_ENA_PIN, OUTPUT);
  pinMode(MOTOR_ENB_PIN, OUTPUT);
}

void get_ir_data() {
  if (ir_receiver.decode(&ir_results)) {
    switch(ir_results.value) {
      case IR_KEY_STOP:    state = STOP;    break;
      case IR_KEY_FORWARD: state = FORWARD; break;
      case IR_KEY_BACK:    state = BACK;    break;
      case IR_KEY_LEFT:    state = LEFT;    break;
      case IR_KEY_RIGHT:   state = RIGHT;   break;
    }
    ir_receiver.resume();
  }
}

void smart_delay(unsigned long t) {
  const unsigned long stop_time = millis() + t;
  do {
    get_ir_data();
    delay(1);
  } while (millis() < stop_time);
}

void forward() {
  analogWrite(MOTOR_ENA_PIN, move_speed);
  analogWrite(MOTOR_ENB_PIN, move_speed);
  digitalWrite(MOTOR_IN1_PIN, HIGH);
  digitalWrite(MOTOR_IN2_PIN, LOW);
  digitalWrite(MOTOR_IN3_PIN, LOW);
  digitalWrite(MOTOR_IN4_PIN, HIGH);
}

void back() {
  analogWrite(MOTOR_ENA_PIN, move_speed);
  analogWrite(MOTOR_ENB_PIN, move_speed);
  digitalWrite(MOTOR_IN1_PIN, LOW);
  digitalWrite(MOTOR_IN2_PIN, HIGH);
  digitalWrite(MOTOR_IN3_PIN, HIGH);
  digitalWrite(MOTOR_IN4_PIN, LOW);
}

void left() {
  analogWrite(MOTOR_ENA_PIN, turn_speed);
  analogWrite(MOTOR_ENB_PIN, turn_speed);
  digitalWrite(MOTOR_IN1_PIN, LOW);
  digitalWrite(MOTOR_IN2_PIN, HIGH);
  digitalWrite(MOTOR_IN3_PIN, LOW);
  digitalWrite(MOTOR_IN4_PIN, HIGH);
}

void right() {
  analogWrite(MOTOR_ENA_PIN, turn_speed);
  analogWrite(MOTOR_ENB_PIN, turn_speed);
  digitalWrite(MOTOR_IN1_PIN, HIGH);
  digitalWrite(MOTOR_IN2_PIN, LOW);
  digitalWrite(MOTOR_IN3_PIN, HIGH);
  digitalWrite(MOTOR_IN4_PIN, LOW);
}

void stop() {
  digitalWrite(MOTOR_ENA_PIN, LOW);
  digitalWrite(MOTOR_ENB_PIN, LOW);
}

void loop() {
  // Put main code here, to run repeatedly:

  if (state == STOP) {
    Serial.println("Stop");
    stop();
    while (state == STOP) {
      smart_delay(1);
    }
  }

  if (state == FORWARD) {
    Serial.println("Forward");
    forward();
    while (state == FORWARD) {
      smart_delay(1);
    }
  }

  if (state == BACK) {
    Serial.println("Back");
    back();
    while (state == BACK) {
      smart_delay(1);
    }
  }

  if (state == LEFT) {
    Serial.println("Left");
    left();
    while (state == LEFT) {
      smart_delay(1);
    }
  }

  if (state == RIGHT) {
    Serial.println("Right");
    right();
    while (state == RIGHT) {
      smart_delay(1);
    }
  }

  smart_delay(1);
}
