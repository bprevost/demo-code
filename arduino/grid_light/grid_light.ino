#include <IRremote.h>
#include <FastLED.h>

// For thermometer
#define TEMP_PIN 0

// For IR remote
#define IR_KEY_UP 16736925
#define IR_KEY_DOWN 16754775
#define IR_KEY_LEFT 16720605
#define IR_KEY_RIGHT 16761405
#define IR_KEY_OK 16712445
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
#define IR_PIN 11
IRrecv ir_receiver(IR_PIN);
decode_results ir_results;

// FOR LED lights
#define LED_PIN 12
#define NUM_LEDS 50
CRGB leds[NUM_LEDS];
byte hue = 255;
byte sat = 255;
byte val = 128;

// HSV colors
const int hsv_black[] = {0, 0, 0};
const int hsv_white[] = {0, 0, 100};
const int hsv_red[] = {0, 100, 100};
const int hsv_green[] = {120, 100, 100};
const int hsv_blue[] = {240, 100, 100};
const int hsv_yellow[] = {60, 100, 100};
const int hsv_cyan[] = {180, 100, 100};
const int hsv_magenta[] = {300, 100, 100};

const byte led_grid[][7] = {
  {6,  7, 20, 21, 34, 35, 48},
  {5,  8, 19, 22, 33, 36, 47},
  {4,  9, 18, 23, 32, 37, 46},
  {3, 10, 17, 24, 31, 38, 45},
  {2, 11, 16, 25, 30, 39, 44},
  {1, 12, 15, 26, 29, 40, 43},
  {0, 13, 14, 27, 28, 41, 42},
};

const byte z_char[7][7] = {
  {1, 1, 1, 1, 1, 1, 1},
  {0, 0, 0, 0, 0, 1, 0},
  {0, 0, 0, 0, 1, 0, 0},
  {0, 0, 0, 1, 0, 0, 0},
  {0, 0, 1, 0, 0, 0, 0},
  {0, 1, 0, 0, 0, 0, 0},
  {1, 1, 1, 1, 1, 1, 1},
};

const byte k_char[7][7] = {
  {1, 1, 0, 0, 0, 1, 1},
  {1, 1, 0, 0, 1, 1, 0},
  {1, 1, 0, 1, 1, 0, 0},
  {1, 1, 1, 1, 0, 0, 0},
  {1, 1, 1, 1, 1, 0, 0},
  {1, 1, 0, 0, 1, 1, 0},
  {1, 1, 0, 0, 0, 1, 1},
};

void setup() {
  ir_receiver.enableIRIn();
  FastLED.addLeds<WS2811, LED_PIN, RGB>(leds, NUM_LEDS);
  Serial.begin(9600);
  Serial.println("Ready");
}

enum STATE {
  OFF,
  ON,
  RAND,
  Z,
  K,
  ZOOM,
  TEMP,
} state = OFF;

void get_ir_data() {
  while (!ir_receiver.isIdle());
  if (ir_receiver.decode(&ir_results)) {
    switch(ir_results.value) {
      case IR_KEY_0:
        state = OFF;
        Serial.println("State set to OFF");
        break;
      case IR_KEY_1:
        state = ON;
        Serial.println("State set to ON");
        break;
      case IR_KEY_2:
        state = RAND;
        Serial.println("State set to RAND");
        break;
      case IR_KEY_3:
        state = Z;
        Serial.println("State set to Z");
        break;
      case IR_KEY_4:
        state = K;
        Serial.println("State set to K");
        break;
      case IR_KEY_5:
        state = ZOOM;
        Serial.println("State set to ZOOM");
        break;
      case IR_KEY_6:
        state = TEMP;
        Serial.println("State set to TEMP");
        break;
      case IR_KEY_UP:
        val += 10;
        if (val > 255) val = 255;
        Serial.print("Val up to ");
        Serial.println(val);
        break;
      case IR_KEY_DOWN:
        val -= 10;
        if (val < 0) val = 0;
        Serial.print("Val down to ");
        Serial.println(val);
        break;
      case IR_KEY_LEFT:
        hue = (256 + hue - 15) % 256;
        Serial.print("Hue down to ");
        Serial.println(hue);
        break;
      case IR_KEY_RIGHT:
        hue = (hue + 15) % 256;
        Serial.print("Hue up to ");
        Serial.println(hue);
        break;
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

void show_digits(int tens_digit, int ones_digit) {
  const byte digit_char[10][5][3] = {
    {  // Zero
      {1, 1, 1},
      {1, 0, 1},
      {1, 0, 1},
      {1, 0, 1},
      {1, 1, 1},
    },
    { // One
      {0, 1, 0},
      {0, 1, 0},
      {0, 1, 0},
      {0, 1, 0},
      {0, 1, 0},
    },
    { // Two
      {1, 1, 1},
      {0, 0, 1},
      {1, 1, 1},
      {1, 0, 0},
      {1, 1, 1},
    },
    { // Three
      {1, 1, 1},
      {0, 0, 1},
      {1, 1, 1},
      {0, 0, 1},
      {1, 1, 1},
    },
    { // Four
      {1, 0, 1},
      {1, 0, 1},
      {1, 1, 1},
      {0, 0, 1},
      {0, 0, 1},
    },
    { // Five
      {1, 1, 1},
      {1, 0, 0},
      {1, 1, 1},
      {0, 0, 1},
      {1, 1, 1},
    },
    { // Six
      {1, 1, 1},
      {1, 0, 0},
      {1, 1, 1},
      {1, 0, 1},
      {1, 1, 1},
    },
    { // Seven
      {1, 1, 1},
      {0, 0, 1},
      {0, 0, 1},
      {0, 0, 1},
      {0, 0, 1},
    },
    { // Eight
      {1, 1, 1},
      {1, 0, 1},
      {1, 1, 1},
      {1, 0, 1},
      {1, 1, 1},
    },
    { // Nine
      {1, 1, 1},
      {1, 0, 1},
      {1, 1, 1},
      {0, 0, 1},
      {0, 0, 1},
    },
  };

  // Clear all the lights
  for (int i = 0; i < NUM_LEDS; i++)
    leds[i] = CHSV(0, 0, 0);

  int row_offset = 1;
  int col_offset = 0;
  for (int row = 0; row < 5; row++)
    for (int col = 0; col < 3; col++)
      if (digit_char[tens_digit][row][col] == 1)
        leds[led_grid[row+row_offset][col+col_offset]] = CHSV(hue, sat, val);

  col_offset = 4;
  for (int row = 0; row < 5; row++)
    for (int col = 0; col < 3; col++)
      if (digit_char[ones_digit][row][col] == 1)
        leds[led_grid[row+row_offset][col+col_offset]] = CHSV(hue, sat, val);

  FastLED.show();
}

void loop() {

  if (state == OFF) {
    // Entry action (happens only once, when entering state)
    Serial.println("Entering OFF state");
    for (int i = 0; i < NUM_LEDS; i++)
      leds[i] = CHSV(0, 0, 0);
    FastLED.show();
    
    while (state == OFF) {
      // State action (happens over and over again, while in the state)
      smart_delay(10);
    }
  }
  
  if (state == ON) {
    // Entry action (happens only once, when entering state)
    Serial.println("Entering ON state");
    
    while (state == ON) {
      // State action (happens over and over again, while in the state)
      for (int i = 0; i < NUM_LEDS-1; i++) // Do not change the last LED
        leds[i] = CHSV(hue, sat, val);
      FastLED.show();
      smart_delay(10);
    }
  }
  
  if (state == RAND) {
    // Entry action (happens only once, when entering state)
    Serial.println("Entering RAND state");
    static uint8_t hues[NUM_LEDS];
    for (auto &h : hues) h = random8();
    
    while (state == RAND) {
      // State action (happens over and over again, while in the state)
      for (int i = 0; i < NUM_LEDS-1; i++) { // Do not change the last LED
        int new_hue = (hues[i] + hue) % 256;
        leds[i] = CHSV(new_hue, sat, val);
      }
      FastLED.show();
      smart_delay(10);
    }
  }

  if (state == Z) {
    // Entry action (happens only once, when entering state)
    Serial.println("Entering Z state");
    
    while (state == Z) {
      // State action (happens over and over again, while in the state)
      for (int row = 0; row < 7; row++) {
        for (int col = 0; col < 7; col++) {
          if (z_char[row][col] == 1) {
            leds[led_grid[row][col]] = CHSV(hue, sat, val);
          } else {
            leds[led_grid[row][col]] = CHSV(0, 0, 0);
          }
        }
      }
      FastLED.show();
      smart_delay(10);
    }
  }

  if (state == K) {
    // Entry action (happens only once, when entering state)
    Serial.println("Entering K state");
    
    while (state == K) {
      // State action (happens over and over again, while in the state)
      for (int row = 0; row < 7; row++) {
        for (int col = 0; col < 7; col++) {
          if (k_char[row][col] == 1) {
            leds[led_grid[row][col]] = CHSV(hue, sat, val);
          } else {
            leds[led_grid[row][col]] = CHSV(0, 0, 0);
          }
        }
      }
      FastLED.show();
      smart_delay(10);
    }
  }

  if (state == ZOOM) {
    // Entry action (happens only once, when entering state)
    Serial.println("Entering ZOOM state");
    
    while (state == ZOOM) {
      // State action (happens over and over again, while in the state)
      int row, col;
      CRGB color1 = leds[led_grid[1][1]];
      CRGB color2 = leds[led_grid[2][2]];
      CRGB color3 = leds[led_grid[3][3]];
      for (row = 0; row < 7; row++)
        for (col = 0; col < 7; col++)
          leds[led_grid[row][col]] = color1;
      for (row = 1; row < 6; row++)
        for (col = 1; col < 6; col++)
          leds[led_grid[row][col]] = color2;
      for (row = 2; row < 5; row++)
        for (col = 2; col < 5; col++)
          leds[led_grid[row][col]] = color3;
      leds[led_grid[3][3]] = CHSV(random8(), sat, val);;
      FastLED.show();
      smart_delay(500);
    }
  }
  
  if (state == TEMP) {
    // Entry action (happens only once, when entering state)
    Serial.println("Entering TEMP state");
    
    while (state == TEMP) {
      // State action (happens over and over again, while in the state)
      int temp_reading = analogRead(TEMP_PIN);
      double tempK = log(10000.0 * ((1024.0 / temp_reading - 1)));
      tempK = 1 / (0.001129148 + (0.000234125 + (0.0000000876741 * tempK * tempK )) * tempK); // Kelvin
      float tempC = tempK - 273.15; // Celcius
      float tempF = (tempC * 9.0)/ 5.0 + 32.0; // Fahrenheit
      Serial.println(tempF, 2);
      int temp = (int)(tempF + 0.5);
      int tens = (int)(temp/10);
      int ones = temp - tens * 10;
      show_digits(tens, ones);
      smart_delay(5000);
    }
  }

}
