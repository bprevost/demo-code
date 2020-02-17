#!/usr/bin/env python3

import board
import neopixel
import signal
import time

run = True
def handler(signal_received, frame):
    global run
    run = False

signal.signal(signal.SIGINT, handler)

NUMPIXELS = 16
pixels = neopixel.NeoPixel(board.D18, NUMPIXELS)
pixels.fill((0, 0, 0))

while run:
    for i in range(NUMPIXELS-1, -1, -1):
        pixels[i] = (255, 0, 0) # Red
        time.sleep(1/NUMPIXELS)
        pixels[i] = (0, 255, 0) # Green

pixels.fill((0, 0, 0))
