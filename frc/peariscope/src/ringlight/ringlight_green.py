#!/usr/bin/env python3

import board
import neopixel

NUMPIXELS = 16

# SPI interface must be enabled through raspi-config
# Use pin BCM10 (physical pin 19)
pixels = neopixel.NeoPixel(board.D10, NUMPIXELS)
pixels.fill((0, 255, 0))
