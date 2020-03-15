#include <IRremote.h>
#include <FastLED.h>

// For IR remote
#define IR_KEY_0 16738455
#define IR_KEY_1 16724175
#define IR_KEY_2 16718055
#define IR_KEY_3 16743045
#define IR_KEY_4 16716015
#define IR_KEY_5 16726215
#define IR_KEY_6 16734885
#define IR_KEY_7 16728765
#define IR_KEY_8 16730805
#define IR_KEY_9 16732845
#define IR_KEY_ON_OFF 16753245
#define IR_KEY_VOL_UP 16736925
#define IR_KEY_VOL_DOWN 16754775
#define IR_KEY_FORWARD 16761405
#define IR_KEY_REVERSE 16720605

// For IR remote
#define IR_PIN 11
IRrecv ir_receiver(IR_PIN);
decode_results ir_results;

// FOR LED lights
#define LED_PIN 12
#define NUM_LEDS 50
CRGB leds[NUM_LEDS];
byte hue = 0;
byte sat = 255;
byte val = 63;

enum STATE {
  OFF,
  SOLID,
} state = OFF;

void setup() {
  ir_receiver.enableIRIn();
  FastLED.addLeds<WS2811, LED_PIN, RGB>(leds, NUM_LEDS);
  Serial.begin(9600);
  Serial.println("Ready");
}

void check_ir() {
  while (!ir_receiver.isIdle()); // Wait until not busy
  if (ir_receiver.decode(&ir_results)) {
    //Serial.println(ir_results.value);
    switch (ir_results.value) {
      case IR_KEY_ON_OFF:
        Serial.println("OFF");
        state = OFF;
        break;
      case IR_KEY_0:
        Serial.println("SOLID");
        state = SOLID;
        break;
    }
    ir_receiver.resume();
  }
}

void loop() {
  delay(1);
  check_ir();

  if (state == OFF) {
    for (int i = 0; i < NUM_LEDS; i++) // For all lights
      leds[i] = CRGB::Black;
    FastLED.show();
    while (state == OFF)
      check_ir();
  }

  if (state == SOLID) {
    while (state == SOLID) {
      for (int i = 0; i < NUM_LEDS - 1; i++) // For all lights except last one
        leds[i] = CHSV(hue, sat, val);
      FastLED.show();
      check_ir();
    }
  }

}
