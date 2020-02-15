#!/usr/bin/env python3

import sys
import board
import neopixel

NUMPIXELS = 50
pixels = neopixel.NeoPixel(board.D21, NUMPIXELS)

if len(sys.argv) == 4:
    red = int(round(float(sys.argv[1])))
    grn = int(round(float(sys.argv[2])))
    blu = int(round(float(sys.argv[3])))
    pixels.fill((grn, red, blu))
elif len(sys.argv) == 2:
    pixels.fill((0, 0, 0))
    index = int(round(float(sys.argv[1])))
    pixels[index] = ((255, 0, 0)) # GRB Green
else:
    pixels.fill((255, 0, 0)) # GRB Green
