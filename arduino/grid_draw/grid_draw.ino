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
#define IR_PIN 11
IRrecv ir_receiver(IR_PIN);
decode_results ir_results;

// FOR LED lights
#define LED_PIN 12
#define NUM_LEDS 50
CRGB leds[NUM_LEDS];
const CRGB blk = CRGB(0, 0, 0);
const CRGB wht = CRGB(64, 64, 64);
const CRGB red = CRGB(64, 0, 0);
const CRGB grn = CRGB(0, 64, 0);
const CRGB blu = CRGB(0, 0, 64);

const byte led_grid[5][10] = {
  { 0,  1,  2,  3,  4,  5,  6,  7,  8,  9},
  {19, 18, 17, 16, 15, 14, 13, 12, 11, 10},
  {20, 21, 22, 23, 24, 25, 26, 27, 28, 29},
  {39, 38, 37, 36, 35, 34, 33, 32, 31, 30},
  {40, 41, 42, 43, 44, 45, 46, 47, 48, 49}
};

// Global variables
int px = 0;
int py = 0;

void check_ir() {
  while (!ir_receiver.isIdle()); // Wait until not busy
  if (ir_receiver.decode(&ir_results)) {
    switch (ir_results.value) {
      case IR_KEY_VOL_UP:
        py = max(py - 1, 0);
        break;
      case IR_KEY_VOL_DOWN:
        py = min(py + 1, 4);
        break;
      case IR_KEY_REVERSE: // Left
        px = max(px - 1, 0);
        break;
      case IR_KEY_FORWARD: // Right
        px = min(px + 1, 9);
        break;
      case IR_KEY_0:
        leds[led_grid[py][px]] = blk;
        break;
      case IR_KEY_1:
        leds[led_grid[py][px]] = red;
        break;
      case IR_KEY_2:
        leds[led_grid[py][px]] = grn;
        break;
      case IR_KEY_3:
        leds[led_grid[py][px]] = blu;
        break;
    }
    ir_receiver.resume();
  }
}

void smart_delay(unsigned long t) {
  const unsigned long stop_time = millis() + t;
  while (millis() < stop_time) {
    check_ir();
    delay(1);
  }
}

void setup() {
  ir_receiver.enableIRIn();
  FastLED.addLeds<WS2811, LED_PIN, RGB>(leds, NUM_LEDS);
  Serial.begin(9600);
  Serial.println("Ready");
  for (int i = 0; i < NUM_LEDS; i++)
    leds[i] = blk;
}

void loop() {
  CRGB val = leds[led_grid[py][px]];
  if (val == CRGB(0, 0, 0))
    leds[led_grid[py][px]] = wht;
  else
    leds[led_grid[py][px]] = blk;
  FastLED.show();
  delay(500);

  leds[led_grid[py][px]] = val;
  FastLED.show();
  smart_delay(500);
 }
 
