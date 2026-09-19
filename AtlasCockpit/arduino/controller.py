import pygame

pygame.init()
pygame.joystick.init()

js = pygame.joystick.Joystick(0)
js.init()

while True:

    pygame.event.pump()

    axis = js.get_axis(1)

    throttle = int(
        ((-axis + 1) / 2) * 100
    )

    print(throttle)