import pygame, time

from util.player import Player
from util.environment import Environment
from util.ui import Button, HealthBar, WinText

from settings.config import RESOLUTION, FPS, DISPLAY_SIZE, update_shift, get_shift

pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
display = pygame.Surface(DISPLAY_SIZE)
clock = pygame.time.Clock()
running = True

environ = Environment(pygame.image.load("assets/environments/env1.png"), DISPLAY_SIZE[1] - 64)

def main_menu():
    darken_layer = pygame.Surface(DISPLAY_SIZE)

    start_button = Button(RESOLUTION[0] - 200, RESOLUTION[1] // 2, 300, 100, "vs battle", game)
    settings_button = Button(RESOLUTION[0] -250, RESOLUTION[1] // 2 + 150, 300, 100, "settings", settings)
    quit_button = Button(RESOLUTION[0] - 300, RESOLUTION[1] // 2 + 300, 300, 100, "quit", pygame.quit)

    while True:
        clock.tick(FPS)
        environ.draw(display)
        darken_layer.fill((0, 0, 0))
        darken_layer.set_alpha(128)
        display.blit(darken_layer, (0, 0))

        mx, my = pygame.mouse.get_pos()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        screen.blit(pygame.transform.scale(display, RESOLUTION), (0, 0))
        
        start_button.update((mx, my))
        start_button.draw(screen)

        settings_button.update((mx, my))
        settings_button.draw(screen)

        quit_button.update((mx, my))
        quit_button.draw(screen)
        pygame.display.flip()

def settings():

    darken_layer = pygame.Surface(DISPLAY_SIZE)

    back_button = Button(RESOLUTION[0] // 2, RESOLUTION[1] // 2 + 300, 300, 100, "back", main_menu)

    edit_player_1 = Button(RESOLUTION[0] // 2 - 200, RESOLUTION[1] // 2, 300, 100, "player 1", edit_player, "player 1")
    edit_player_2 = Button(RESOLUTION[0] // 2 + 200, RESOLUTION[1] // 2, 300, 100, "player 2", edit_player, "player 2")

    while True:
        clock.tick(FPS)
        environ.draw(display)
        darken_layer.fill((0, 0, 0))
        darken_layer.set_alpha(128)
        display.blit(darken_layer, (0, 0))

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        screen.blit(pygame.transform.scale(display, RESOLUTION), (0, 0))
        
        back_button.update((mx, my))
        back_button.draw(screen)

        edit_player_1.update((mx, my))
        edit_player_1.draw(screen)

        edit_player_2.update((mx, my))
        edit_player_2.draw(screen)

        pygame.display.flip()

def edit_player(player):
    
    darken_layer = pygame.Surface(DISPLAY_SIZE)

    back_button = Button(RESOLUTION[0] // 2, RESOLUTION[1] // 2 + 300, 300, 100, "back", settings)

    text = "edit " + player
    font = pygame.font.Font('assets\\font\\tarrgetexpandital.ttf', 64)
    text = font.render(text, True, (255, 255, 255))

    shift_slider = pygame.Rect(0, 0, 100, 10)
    shift_slider.center = (DISPLAY_SIZE[0] // 2, 40)

    shift_slider_slide = pygame.Rect(0, 0, 10, 10)
    shift_slider_slide.center = (DISPLAY_SIZE[0] // 2, 40)

    slider_selected = False

    playerpreview = Player(DISPLAY_SIZE[0] // 2 - 132 if player == "player 2" else DISPLAY_SIZE[0] // 2 + 132, 80, 64, 96, "assets/player1/spritesheet.png", healthbar=None, side="left" if player == "player 2" else "right", frozen=True)
    print('edit player')

    # get shift value
    shift_value = get_shift(player)
    shift_position = shift_value / 180 * shift_slider.width + shift_slider.left
    shift_slider_slide.center = (shift_position, 40)

    update_counter = 0

    while True:
        clock.tick(FPS)
        environ.draw(display)
        darken_layer.fill((0, 10, 0))
        darken_layer.set_alpha(128)
        display.blit(darken_layer, (0, 0))

        mx, my = pygame.mouse.get_pos()
        smx, smy = pygame.mouse.get_pos()[0] // 4, pygame.mouse.get_pos()[1] // 4

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if shift_slider.collidepoint(smx, smy):
                    shift_slider_slide.center = (smx, 40)
                    slider_selected = True
            if event.type == pygame.MOUSEMOTION:
                if shift_slider.collidepoint(smx, smy) and slider_selected:
                    shift_slider_slide.center = (smx, 40)
            if event.type == pygame.MOUSEBUTTONUP:
                slider_selected = False
        
        # shift value so that when the slider is at the leftmost, the shift value is 0 and when it is at the rightmost, the shift value is 180
        shift_value = int((shift_slider_slide.center[0] - shift_slider.left) / shift_slider.width * 180)
        # print(shift_value)
        update_shift(player, shift_value)
        
        # update every half second
        if update_counter >= 30:
            playerpreview.refresh_shift()
            update_counter = 0
        playerpreview.update(0)
        playerpreview.draw(display)
        print(update_counter)
        update_counter += 1
            
        pygame.draw.rect(display, (255, 255, 255), shift_slider)
        pygame.draw.rect(display, (100, 45, 90), shift_slider_slide)

        screen.blit(pygame.transform.scale(display, RESOLUTION), (0, 0))

        screen.blit(text, (RESOLUTION[0] // 2 - text.get_width() // 2, 50))
        
        back_button.update((mx, my))
        back_button.draw(screen)

        pygame.display.flip()

def game():
    # delta time initialization
    dt = 0
    prev_time = time.time()
    
    healthbar1 = HealthBar("left", 10, 10, 100, 10, 100)
    healthbar2 = HealthBar("right", DISPLAY_SIZE[0] - 110, 10, 100, 10, 100, flipped=True)

    player = Player(DISPLAY_SIZE[0] // 2 - 132, 80, 64, 96, "assets/player1/spritesheet.png", healthbar=healthbar1, side="left" )
    player2 = Player(DISPLAY_SIZE[0] // 2 + 100, 80, 64, 96, "assets/player1/spritesheet.png", healthbar=healthbar2, side="right" )

    player.set_enemy(player2)
    player2.set_enemy(player)

    won = False
    winner = None

    darken_layer = pygame.Surface(DISPLAY_SIZE)

    while True:
        clock.tick(FPS)
        environ.draw(display)

        # darken
        darken_layer.fill((0, 0, 0))
        darken_layer.set_alpha(128)

        # compute delta time
        now = time.time()
        dt = now - prev_time
        prev_time = now

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        if player.health <= 0:
            won = True
            winner = 2
            display.blit(darken_layer, (0, 0))
        elif player2.health <= 0:
            won = True
            winner = 1
            display.blit(darken_layer, (0, 0))
            print("player 1 wins")
        else:
            player.update(dt)
            player2.update(dt)

        player.draw(display)
        player2.draw(display)

        healthbar1.draw(display)
        healthbar2.draw(display)

        print(player.health, player2.health)

        screen.blit(pygame.transform.scale(display, RESOLUTION), (0, 0))
        if won:
            win_text = WinText(winner)
            win_text.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
    pygame.quit()
