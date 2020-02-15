#!/usr/bin/env python3

import board
import neopixel

NUMPIXELS = 50
pixels = neopixel.NeoPixel(board.D21, NUMPIXELS)

pixels.fill((0, 0, 0)) # Turn off pixels
