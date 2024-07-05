import pygame, time
from settings.config import RESOLUTION, FPS

pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()
running = True

# delta time initialization
dt = 0
prev_time = time.time()


while running:
    clock.tick(60)
    # compute delta time
    now = time.time()
    dt = now - prev_time
    prev_time = now

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")

    pygame.display.flip()

pygame.quit()