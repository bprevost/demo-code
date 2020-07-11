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
CRGB blk = CRGB(0, 0, 0);
CRGB red = CRGB(64, 0, 0);
CRGB grn = CRGB(0, 64, 0);
CRGB blu = CRGB(0, 0, 64);
CRGB yel = CRGB(64, 64, 0);

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
int tx = 0;
int ty = 0;
bool start = true;

void check_ir() {
  while (!ir_receiver.isIdle()); // Wait until not busy
  if (ir_receiver.decode(&ir_results)) {
    switch (ir_results.value) {
      case IR_KEY_VOL_UP:
        Serial.println("IR_KEY_VOL_UP");
        // Clear old position
        leds[led_grid[py][px]] = blk;
        FastLED.show();
        // Update position and display
        py = max(py - 1, 0);
        leds[led_grid[py][px]] = grn;
        FastLED.show();
        break;
      case IR_KEY_VOL_DOWN:
        Serial.println("IR_KEY_VOL_DOWN");
        // Clear old position
        leds[led_grid[py][px]] = blk;
        FastLED.show();
        // Update position and display
        py = min(py + 1, 4);
        leds[led_grid[py][px]] = grn;
        FastLED.show();
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
}

void loop() {

  if (start) {
    start = false;
    // Clear the board
    for (int i = 0; i < NUM_LEDS; i++)
      leds[i] = blk;
    // Put player in position
    leds[led_grid[py][px]] = grn;
    // Create target
    tx = 9;
    ty = random(5);
    leds[led_grid[ty][tx]] = red;
  } else {
    // Update target position
    leds[led_grid[ty][tx]] = blk;
    tx = max(tx - 1, 0);
    if (tx > px) {
      // Travelling
      leds[led_grid[ty][tx]] = red;
    } else if (ty != py) {
      // Miss
      leds[led_grid[ty][tx]] = red;
      start = true;
    } else {
      // Hit
      leds[led_grid[ty][tx]] = yel;
      start = true;
    }
  }

  FastLED.show();
  smart_delay(500);
}
