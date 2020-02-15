#!/usr/bin/env python3

import board
import neopixel

from time import sleep
from colorsys import rgb_to_hsv, hsv_to_rgb
from random import randint
from gridfonts import GridFonts

class GridLight:

    RGB_BLACK = (0, 0, 0)
    RGB_WHITE = (255, 255, 255)
    RGB_RED = (255, 0, 0)
    RGB_GREEN = (0, 255, 0)
    RGB_BLUE = (0, 0, 255)
    RGB_CYAN = (0, 255, 255)
    RGB_MAGENTA = (255, 0, 255)
    RGB_YELLOW = (255, 255, 0)

    GRID = [
        [44, 43, 32, 31, 20, 19, 8],
        [45, 42, 33, 30, 21, 18, 9],
        [46, 41, 34, 29, 22, 17, 10],
        [47, 40, 35, 28, 23, 16, 11],
        [48, 39, 36, 27, 24, 15, 12],
        [49, 38, 37, 26, 25, 14, 13],
    ]

    def __init__(self, num_lights=50):
        self.num_lights = num_lights
        self.lights_grb = neopixel.NeoPixel(board.D21, self.num_lights)
        self.grid_fonts = GridFonts()

    def rgb_to_brg(self, rgb):
        return(rgb[1], rgb[0], rgb[2])

    def all_off(self):
        self.lights_grb.fill((0, 0, 0))

    def all_rgb(self, rgb):
        self.lights_grb.fill(self.rgb_to_brg(rgb))

    def set_rgb(self, i, rgb):
        rgb = (int(rgb[0]), int(rgb[1]),  int(rgb[2])) # Convert to integer
        self.lights_grb[i] = self.rgb_to_brg(rgb)

    def all_xmas(self):
        for i in range(0, self.num_lights, 5):
            self.set_rgb(i,   self.RGB_RED)
            self.set_rgb(i+1, self.RGB_GREEN)
            self.set_rgb(i+2, self.RGB_MAGENTA)
            self.set_rgb(i+3, self.RGB_BLUE)
            self.set_rgb(i+4, self.RGB_YELLOW)

    def flicker_random(self):
        # Pick random light
        id = randint(0, self.num_lights-1)

        # Get the current color of the light
        g, r, b = self.lights_grb[id]
        h, s, v = rgb_to_hsv(r, g, b)

        # Flicker the light
        for j in range(10):
            self.set_rgb(id, hsv_to_rgb(h, s, randint(0, 128)))
            sleep(randint(0, 10) / 100.0)

        # Return the light to its original state
        self.set_rgb(id, (r, g, b))

    def draw(self, char, foreground=RGB_WHITE, background=RGB_BLACK):
        print("Drawing", char)
        font = self.grid_fonts.char[char]
        for row in range(len(font)):
            for col in range(len(font[row])):
                index = self.GRID[row][col]
                if font[row][col] == 0:
                    self.set_rgb(index, background)
                else:
                    self.set_rgb(index, foreground)

if __name__ == "__main__":
    grid_light = GridLight()

    while True:
        for char in grid_light.grid_fonts.char:
            grid_light.draw(char, grid_light.RGB_BLUE, grid_light.RGB_MAGENTA)
            sleep(1)

    quit()

    print("Turning all lights off...")
    grid_light.all_off()

    sleep(2)
    print("Turning all lights to green...")
    grid_light.all_rgb(grid_light.RGB_GREEN)

    sleep(2)
    print("Turning all lights to Christmas colors...")
    grid_light.all_xmas()

    sleep(2)
    print("Flickering some random lights...")
    grid_light.flicker_random()
    grid_light.flicker_random()
    grid_light.flicker_random()

    sleep(2)
    print("Turning all lights off...")
    grid_light.all_off()
