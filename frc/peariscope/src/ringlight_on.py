#!/usr/bin/env python3

import board
import neopixel
import sys

if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "red grn blu")
    print("  red: the red intensity (0 to 255)")
    print("  grn: the green intensity (0 to 255)")
    print("  blu: the blue intensity (0 to 255)")
    sys.exit(1)

NUMPIXELS = 16
pixels = neopixel.NeoPixel(board.D18, NUMPIXELS)
red = int(round(float(sys.argv[1])))
grn = int(round(float(sys.argv[2])))
blu = int(round(float(sys.argv[3])))
pixels.fill((red, grn, blu))
