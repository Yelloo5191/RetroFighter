import pygame
from enum import Enum

RESOLUTION = (1280, 720)
DISPLAY_SIZE = (320, 180)
FPS = 60

player1_shift = 180
player2_shift = 40

def update_shift(player, value):
    global player1_shift, player2_shift
    if player == "player 1" and value != player2_shift:
        player1_shift = value
    elif player == "player 2" and value != player1_shift:
        player2_shift = value

def get_shift(player):
    if player == "player 1":
        return player1_shift
    elif player == "player 2":
        return player2_shift

class Player_Input_1(Enum):
    MOVE_LEFT = pygame.K_j
    MOVE_RIGHT = pygame.K_l
    JUMP = pygame.K_i
    CROUCH = pygame.K_k
    ATTACK_1 = pygame.K_LEFT
    ATTACK_2 = pygame.K_RIGHT
    ATTACK_3 = pygame.K_UP
    ATTACK_4 = pygame.K_DOWN


class Player_Input_2(Enum):
    MOVE_LEFT = pygame.K_a
    MOVE_RIGHT = pygame.K_d
    JUMP = pygame.K_w
    CROUCH = pygame.K_s
    ATTACK_1 = pygame.K_v
    ATTACK_2 = pygame.K_n
    ATTACK_3 = pygame.K_g
    ATTACK_4 = pygame.K_b
