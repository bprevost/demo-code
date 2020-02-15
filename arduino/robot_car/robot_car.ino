#include <IRremote.h>
#include <Servo.h>

// For IR remote
#define IR_KEY_FORWARD 16736925
#define IR_KEY_BACK 16754775
#define IR_KEY_LEFT 16720605
#define IR_KEY_RIGHT 16761405
#define IR_KEY_STOP 16712445
#define IR_KEY_1 16738455
#define IR_KEY_2 16750695
#define IR_KEY_3 16756815
#define IR_KEY_4 16724175
#define IR_KEY_5 16718055
#define IR_KEY_6 16743045
#define IR_KEY_7 16716015
#define IR_KEY_8 16726215
#define IR_KEY_9 16734885
#define IR_KEY_0 16730805
#define IR_KEY_STAR 16728765
#define IR_KEY_HASH 16732845

// For IR remote
#define IR_PIN 12
IRrecv ir_receiver(IR_PIN);
decode_results ir_results;

// For motors
#define MOTOR_ENA_PIN 5
#define MOTOR_ENB_PIN 6
#define MOTOR_IN1_PIN 7
#define MOTOR_IN2_PIN 8
#define MOTOR_IN3_PIN 9
#define MOTOR_IN4_PIN 11

// For line tracking
#define LINE_TRACKING_PIN_LEFT 2
#define LINE_TRACKING_PIN_CENTER 4
#define LINE_TRACKING_PIN_RIGHT 10
#define LINE_TRACKING_READ_LEFT !digitalRead(LINE_TRACKING_PIN_LEFT)
#define LINE_TRACKING_READ_CENTER !digitalRead(LINE_TRACKING_PIN_CENTER)
#define LINE_TRACKING_READ_RIGHT !digitalRead(LINE_TRACKING_PIN_RIGHT)

// For servo
#define SERVO_PIN 3
#define SERVO_MIN 530 // The pulse width, in microseconds, corresponding to the minimum (0-degree) angle on the servo
#define SERVO_MAX 2850 // The pulse width, in microseconds, corresponding to the maximum (180-degree) angle on the servo
Servo servo;

// For ultrasonic sensor
#define ULTRASONIC_ECHO_PIN A4
#define ULTRASONIC_TRIG_PIN A5

// Global variables
const int move_speed = 100; // [0, 255]
const int turn_speed = 128; // [0, 255]
const int stop_dist_cm = 10; // Stopping distance for ultrasonic sensor

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

  // For built-in LED
  pinMode(LED_BUILTIN, OUTPUT);

  // For motors
  pinMode(MOTOR_IN1_PIN, OUTPUT);
  pinMode(MOTOR_IN2_PIN, OUTPUT);
  pinMode(MOTOR_IN3_PIN, OUTPUT);
  pinMode(MOTOR_IN4_PIN, OUTPUT);
  pinMode(MOTOR_ENA_PIN, OUTPUT);
  pinMode(MOTOR_ENB_PIN, OUTPUT);

  // For line tracking
  pinMode(LINE_TRACKING_PIN_LEFT, INPUT);
  pinMode(LINE_TRACKING_PIN_CENTER, INPUT);
  pinMode(LINE_TRACKING_PIN_RIGHT, INPUT);

  // For servo
  servo.attach(SERVO_PIN, SERVO_MIN, SERVO_MAX);
  servo.write(85);

  // For ultrasonic sensor
  pinMode(ULTRASONIC_ECHO_PIN, INPUT);
  pinMode(ULTRASONIC_TRIG_PIN, OUTPUT);
}

void get_serial_data() {
  if (Serial.available()) {
    switch (Serial.read()) {
      case 's': state = STOP;    break;
      case 'f': state = FORWARD; break;
      case 'b': state = BACK;    break;
      case 'l': state = LEFT;    break;
      case 'r': state = RIGHT;   break;
      case '1': break;
      case '2': break;
    }
  }
}

void get_ir_data() {
  if (ir_receiver.decode(&ir_results)) {
    switch(ir_results.value) {
      case IR_KEY_STOP:    state = STOP;    break;
      case IR_KEY_FORWARD: state = FORWARD; break;
      case IR_KEY_BACK:    state = BACK;    break;
      case IR_KEY_LEFT:    state = LEFT;    break;
      case IR_KEY_RIGHT:   state = RIGHT;   break;
      case IR_KEY_1:       break;
      case IR_KEY_2:       break;
    }
    ir_receiver.resume();
  }
}

void flash_led(unsigned long count) {
  for (unsigned long i = 0; i < count; i++) {
      digitalWrite(LED_BUILTIN, HIGH); // Turn on the built-in LED
      smart_delay(50);
      digitalWrite(LED_BUILTIN, LOW); // Turn off the built-in LED
      smart_delay(50);
  }
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

int get_distance() {
  digitalWrite(ULTRASONIC_TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(ULTRASONIC_TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(ULTRASONIC_TRIG_PIN, LOW);
  return (int)pulseIn(ULTRASONIC_ECHO_PIN, HIGH) / 58;
}

void smart_delay(unsigned long t) {
  const unsigned long stop_time = millis() + t;
  do {
    get_serial_data();
    get_ir_data();
    delay(1);
  } while (millis() < stop_time);
}

void loop() {
  // Put main code here, to run repeatedly:

  //
  // STOP State
  //

  if (state == STOP) {
    // State setup
    stop(); // Stop the wheel motors
    
    // State loop
    while (state == STOP) {
      smart_delay(1);
    }
  }

  //
  // FORWARD State
  //

  if (state == FORWARD) {
    // State setup
    forward(); // Start moving forward
    
    // State loop
    while (state == FORWARD) {
      // Stop if line tracker sees a line (or edge of table)
      if (LINE_TRACKING_READ_LEFT || LINE_TRACKING_READ_CENTER || LINE_TRACKING_READ_RIGHT) {
        state = STOP;
        flash_led(1);
        break;
      }
      if (get_distance() < stop_dist_cm) {
        state = STOP;
        flash_led(2);
        break;
      }
      smart_delay(1);
    }
  }

  //
  // BACK State
  //

  if (state == BACK) {
    // State setup
    back(); // Start moving reverse
    
    // State loop
    while (state == BACK) {
      smart_delay(1);
    }
  }

  //
  // LEFT State
  //

  if (state == LEFT) {
    // State setup
    left(); // Start turning left
    
    // State loop
    while (state == LEFT) {
      smart_delay(1);
    }
  }

  //
  // RIGHT State
  //

  if (state == RIGHT) {
    // State setup
    right(); // Start turning right
    
    // State loop
    while (state == RIGHT) {
      smart_delay(1);
    }
  }

}
