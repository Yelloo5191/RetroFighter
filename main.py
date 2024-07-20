import pygame, time

from util.player import Player
from util.environment import Environment
from util.ui import Button, HealthBar

from settings.config import RESOLUTION, FPS, DISPLAY_SIZE

pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
display = pygame.Surface(DISPLAY_SIZE)
clock = pygame.time.Clock()
running = True

environ = Environment(pygame.image.load("assets/environments/env1.png"), DISPLAY_SIZE[1] - 64)

def main_menu():
    darken_layer = pygame.Surface(DISPLAY_SIZE)

    start_button = Button(160, 90, 75, 25, "VS Battle", game)
    quit_button = Button(170, 120, 75, 25, "Quit", pygame.quit)

    while True:
        clock.tick(FPS)
        environ.draw(display)
        darken_layer.fill((0, 0, 0))
        darken_layer.set_alpha(128)
        display.blit(darken_layer, (0, 0))

        mx, my = pygame.mouse.get_pos()
        # normalize mouse position to display size
        mx = mx * (DISPLAY_SIZE[0] / RESOLUTION[0])
        my = my * (DISPLAY_SIZE[1] / RESOLUTION[1])

        start_button.update((mx, my))
        start_button.draw(display)

        quit_button.update((mx, my))
        quit_button.draw(display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        screen.blit(pygame.transform.scale(display, RESOLUTION), (0, 0))
        pygame.display.flip()

def game():
    # delta time initialization
    dt = 0
    prev_time = time.time()
    
    healthbar1 = HealthBar("left", 10, 10, 100, 10, 100)
    healthbar2 = HealthBar("right", DISPLAY_SIZE[0] - 110, 10, 100, 10, 100)

    player = Player(DISPLAY_SIZE[0] // 2 - 132, 80, 64, 96, "assets/player1/spritesheet.png", healthbar=healthbar1, side="left", debug=True)
    player2 = Player(DISPLAY_SIZE[0] // 2 + 100, 80, 64, 96, "assets/player1/spritesheet.png", healthbar=healthbar2, side="right", debug=True)

    player.set_enemy(player2)
    player2.set_enemy(player)


    while True:
        clock.tick(FPS)
        environ.draw(display)

        # compute delta time
        now = time.time()
        dt = now - prev_time
        prev_time = now

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        player.update(dt)
        player.draw(display)
        player2.update(dt)
        player2.draw(display)

        healthbar1.draw(display)
        healthbar2.draw(display)

        screen.blit(pygame.transform.scale(display, RESOLUTION), (0, 0))
        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
    pygame.quit()
