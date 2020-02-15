#!/usr/bin/env python3

import os
import sys
import board
import neopixel
import time
import signal

def handler(signal_received, frame):
    # Turn off the lights and exit when ctrl-C is pressed
    for i in range(NUMPIXELS):
        pixels[i] = (0, 0, 0)
    sys.exit(0)

if os.geteuid() != 0:
    print("usage: sudo", sys.argv[0])
    sys.exit(1)

NUMPIXELS = 93
pixels = neopixel.NeoPixel(board.D18, NUMPIXELS)
signal.signal(signal.SIGINT, handler)

row1 = range(32+24+16+12+8, 32+24+16+12+8+1)
row2 = range(32+24+16+12, 32+24+16+12+8)
row3 = range(32+24+16, 32+24+16+12)
row4 = range(32+24, 32+24+16)
row5 = range(32, 32+24)
row6 = range(0, 0+32)

allrows = [row1, row2, row3, row4, row5, row6]

for row in allrows:
    for i in row:
        pixels[i] = (0, 0, 0) # Black

for i in row1:
    pixels[i] = (7, 0, 0) # Red

for i in row2:
    pixels[i] = (0, 7, 0) # Green

for i in row3:
    pixels[i] = (0, 0, 7) # Blue

for i in row4:
    pixels[i] = (7, 7, 0) # Yellow

for i in row5:
    pixels[i] = (7, 0, 7) # Magenta

for i in row6:
    pixels[i] = (0, 7, 7) # Cyan

