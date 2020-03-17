#include <IRremote.h>
#include <FastLED.h>

// For thermometer
#define TEMP_PIN 0

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
  {1, 1, 1, 1, 1, 1, 0},
  {0, 0, 0, 1, 1, 0, 0},
  {0, 0, 1, 1, 0, 0, 0},
  {0, 1, 1, 0, 0, 0, 0},
  {1, 1, 1, 1, 1, 1, 1},
  {1, 1, 1, 1, 1, 1, 1},
};

const byte k_char[7][7] = {
  {1, 1, 0, 0, 0, 1, 1},
  {1, 1, 0, 0, 1, 1, 0},
  {1, 1, 1, 1, 1, 0, 0},
  {1, 1, 1, 1, 0, 0, 0},
  {1, 1, 0, 1, 1, 0, 0},
  {1, 1, 0, 0, 1, 1, 0},
  {1, 1, 0, 0, 0, 1, 1},
};


// black (0), red (1), white (2), blue (3)
const byte tx_char[7][7] = {
  {0, 0, 3, 3, 0, 0, 0},
  {0, 0, 3, 3, 0, 0, 0},
  {0, 0, 3, 3, 2, 2, 2},
  {3, 3, 2, 3, 2, 2, 2},
  {0, 3, 3, 3, 1, 1, 1},
  {0, 0, 0, 3, 1, 1, 0},
  {0, 0, 0, 0, 1, 0, 0},
};

enum STATE {
  OFF,
  SOLID,
  RANDOM,
  Z,
  K,
  ZOOM,
  TEMP,
  WHITE,
  TEXAS,
} state = TEXAS;

bool change = true; // Trigger a light update?

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
        change = true;
        if (state == OFF) {
          state = SOLID;
          Serial.println("SOLID");
        } else {
          state = OFF;
          Serial.println("OFF");
        }
        break;

      case IR_KEY_0:
        change = true;
        state = OFF;
        Serial.println("OFF");
        break;
      case IR_KEY_1:
        change = true;
        state = SOLID;
        Serial.println("SOLID");
        break;
      case IR_KEY_2:
        change = true;
        state = RANDOM;
        Serial.println("RANDOM");
        break;
      case IR_KEY_3:
        change = true;
        state = Z;
        Serial.println("Z");
        break;
      case IR_KEY_4:
        change = true;
        state = K;
        Serial.println("K");
        break;
      case IR_KEY_5:
        change = true;
        state = TEXAS;
        Serial.println("TEXAS");
        break;
      case IR_KEY_6:
        change = true;
        state = ZOOM;
        Serial.println("ZOOM");
        break;
      case IR_KEY_7:
        change = true;
        state = TEMP;
        Serial.println("TEMP");
        break;
      case IR_KEY_8:
        change = true;
        state = WHITE;
        Serial.println("WHITE");
        break;

      case IR_KEY_VOL_UP:
        change = true;
        val = min(val + 16, 255);
        Serial.print("Val up to ");
        Serial.println(val);
        break;
      case IR_KEY_VOL_DOWN:
        change = true;
        val = max(val - 16, 0);
        Serial.print("Val down to ");
        Serial.println(val);
        break;
      case IR_KEY_FORWARD:
        change = true;
        hue = (256 + hue + 16) % 256;
        Serial.print("Hue up to ");
        Serial.println(hue);
        break;
      case IR_KEY_REVERSE:
        change = true;
        hue = (256 + hue - 16) % 256;
        Serial.print("Hue down to ");
        Serial.println(hue);
        break;

    }
    ir_receiver.resume();
  }
}

void smart_delay(unsigned long t) {
  const unsigned long stop_time = millis() + t;
  do {
    check_ir();
    delay(1);
  } while (millis() < stop_time);
}

void show_digits(int tens_digit, int ones_digit) {
  const byte digit_char[10][5][3] = {
    { // Zero
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
        leds[led_grid[row + row_offset][col + col_offset]] = CHSV(hue, sat, val);

  col_offset = 4;
  for (int row = 0; row < 5; row++)
    for (int col = 0; col < 3; col++)
      if (digit_char[ones_digit][row][col] == 1)
        leds[led_grid[row + row_offset][col + col_offset]] = CHSV(hue, sat, val);

  FastLED.show();
}

void loop() {
  smart_delay(1);

  while (state == OFF) {
    if (change == true) {
      for (int i = 0; i < NUM_LEDS; i++) // For all lights
        leds[i] = CRGB::Black;
      FastLED.show();
      change = false;
    }
    smart_delay(1);
  }

  while (state == SOLID) {
    if (change == true) {
      for (int i = 0; i < NUM_LEDS - 1; i++) // For all lights except last one
        leds[i] = CHSV(hue, sat, val);
      FastLED.show();
      change = false;
    }
    smart_delay(1);
  }

  while (state == RANDOM) {
    if (change == true) {
      static uint8_t hues[NUM_LEDS];
      for (auto &h : hues) h = random8();
      for (int i = 0; i < NUM_LEDS - 1; i++) // For all lights except last one
        leds[i] = CHSV(hues[i], sat, val);
      FastLED.show();
      change = false;
    }
    smart_delay(1);
  }

  while (state == Z) {
    if (change == true) {
      for (int row = 0; row < 7; row++)
        for (int col = 0; col < 7; col++)
          if (z_char[row][col] == 1)
            leds[led_grid[row][col]] = CHSV(hue, sat, val);
          else
            leds[led_grid[row][col]] = CRGB::Black;
      FastLED.show();
      change = false;
    }
    smart_delay(1);
  }

  while (state == K) {
    if (change == true) {
      for (int row = 0; row < 7; row++)
        for (int col = 0; col < 7; col++)
          if (k_char[row][col] == 1)
            leds[led_grid[row][col]] = CHSV(hue, sat, val);
          else
            leds[led_grid[row][col]] = CRGB::Black;
      FastLED.show();
      change = false;
    }
    smart_delay(1);
  }

  while (state == TEXAS) {
    if (change == true) {
      for (int row = 0; row < 7; row++)
        for (int col = 0; col < 7; col++)
          if (tx_char[row][col] == 1)
            leds[led_grid[row][col]] = CRGB::Red;
          else if (tx_char[row][col] == 2)
            leds[led_grid[row][col]] = CRGB::White;
          else if (tx_char[row][col] == 3)
            leds[led_grid[row][col]] = CRGB::Blue;
          else
            leds[led_grid[row][col]] = CRGB::Black;
      for (int i = 0; i < NUM_LEDS - 1; i++) { // For all lights except last one
        leds[i].maximizeBrightness();
        leds[i].nscale8(val);
      }
      FastLED.show();
      change = false;
    }
    smart_delay(250);
    leds[led_grid[3][2]] = CRGB::Blue;
    leds[led_grid[3][2]].maximizeBrightness();
    leds[led_grid[3][2]].nscale8(val);
    FastLED.show();

    smart_delay(250);
    leds[led_grid[3][2]] = CRGB::White;
    leds[led_grid[3][2]].maximizeBrightness();
    leds[led_grid[3][2]].nscale8(val);
    FastLED.show();
  }

  while (state == ZOOM) {
    CRGB color1 = leds[led_grid[1][1]];
    CRGB color2 = leds[led_grid[2][2]];
    CRGB color3 = leds[led_grid[3][3]];
    int row, col;
    for (row = 0; row < 7; row++)
      for (col = 0; col < 7; col++)
        leds[led_grid[row][col]] = color1;
    for (row = 1; row < 6; row++)
      for (col = 1; col < 6; col++)
        leds[led_grid[row][col]] = color2;
    for (row = 2; row < 5; row++)
      for (col = 2; col < 5; col++)
        leds[led_grid[row][col]] = color3;
    leds[led_grid[3][3]] = CHSV(random8(), sat, val);
    FastLED.show();
    smart_delay(500);
  }

  while (state == TEMP) {
    int temp_reading = analogRead(TEMP_PIN);
    double tempK = log(10000.0 * ((1024.0 / temp_reading - 1)));
    tempK = 1 / (0.001129148 + (0.000234125 + (0.0000000876741 * tempK * tempK )) * tempK); // Kelvin
    float tempC = tempK - 273.15; // Celcius
    float tempF = (tempC * 9.0) / 5.0 + 32.0; // Fahrenheit
    int temp = (int)(tempF + 0.5);
    int tens = (int)(temp / 10);
    int ones = temp - tens * 10;
    show_digits(tens, ones);
    smart_delay(1000);
  }

  while (state == WHITE) {
    if (change == true) {
      for (int i = 0; i < NUM_LEDS - 1; i++) // For all lights except last one
        leds[i] = CRGB::White;
      FastLED.show();
      change = false;
    }
    smart_delay(1);
  }
}
