// Stranger LEDs
// Spells a word by flashing lights from a WS2811 LED light string.

#include <FastLED.h>

#define NUM_LEDS 50 // Number of LEDs on the WS2811 LED light string
#define DATA_PIN 12 // Data pin on the Adruino used to control the lights

// The locations of individual letters on the light string
#define A 10
#define B 12
#define C 34
#define D 37
#define E 9
#define F 14
#define G 32
#define H 39
#define I 7
#define J 16
#define K 30
#define L 41
#define M 5
#define N 17
#define O 28
#define P 43
#define Q 4
#define R 19
#define S 26
#define T 45
#define U 2
#define V 24
#define W 46
#define X 0
#define Y 23
#define Z 49

CRGB leds[NUM_LEDS];
uint8_t hues[NUM_LEDS];

void setup()
{
  FastLED.addLeds<WS2811, DATA_PIN, RGB>(leds, NUM_LEDS);
  for (auto &h : hues) h = random8();
}

uint8_t get_index(char c)
{
  switch (toUpperCase(c))
  {
    case 'A': return A;
    case 'B': return B;
    case 'C': return C;
    case 'D': return D;
    case 'E': return E;
    case 'F': return F;
    case 'G': return G;
    case 'H': return H;
    case 'I': return I;
    case 'J': return J;
    case 'K': return K;
    case 'L': return L;
    case 'M': return M;
    case 'N': return N;
    case 'O': return O;
    case 'P': return P;
    case 'Q': return Q;
    case 'R': return R;
    case 'S': return S;
    case 'T': return T;
    case 'U': return U;
    case 'V': return V;
    case 'W': return W;
    case 'X': return X;
    case 'Y': return Y;
    case 'Z': return Z;
  }
}

void display_led(uint8_t index)
{
  for (int i = 0; i < 4; i++)
  {
    leds[index] = CHSV(hues[index], 255, 255);
    FastLED.show();
    delay(random8()/2);
    
    leds[index] = CRGB::Black;
    FastLED.show();
    delay(random8());
  }
}

void message(const char *str)
{
  while (*str)
  {
    if (isAlpha(*str))
    {
      display_led(get_index(*str));
      delay(500);
    }
    else if (isSpace(*str))
    {
      delay(1000);
    }
    str++;
  }
}

void loop()
{
  message("abcdefghijklmnopqrstuvwxyz");
  delay(1000);
}
