import pygame

pygame.init()
clock = pygame.time.Clock()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

while True:
    pygame.event.pump()
    neck_axis = joystick.get_axis(1)
    head_axis = joystick.get_axis(2)
    print neck_axis, head_axis
    clock.tick(20)

pygame.quit()
