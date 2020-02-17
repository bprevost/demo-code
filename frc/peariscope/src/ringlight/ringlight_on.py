#!/usr/bin/env python3

import board
import neopixel
import sys

NUMPIXELS = 16

if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "red grn blu")
    print("  red: the red intensity (0 to 255)")
    print("  grn: the green intensity (0 to 255)")
    print("  blu: the blue intensity (0 to 255)")
    sys.exit(1)

# SPI interface must be enabled through raspi-config
# Use pin BCM10 (physical pin 19)
pixels = neopixel.NeoPixel(board.D10, NUMPIXELS)
red = int(sys.argv[1])
grn = int(sys.argv[2])
blu = int(sys.argv[3])
pixels.fill((red, grn, blu))
