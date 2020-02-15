#!/usr/bin/env python3

import sys
import time
import pygame

pygame.init()

width, height = 600, 400
speed = [4, 4]
black = 0, 0, 0

screen = pygame.display.set_mode((width, height))
ball = pygame.image.load("ball.gif")
ballrect = ball.get_rect()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()
    time.sleep(0.01)
