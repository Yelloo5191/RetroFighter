import pygame
from enum import Enum

RESOLUTION = (1280, 720)
DISPLAY_SIZE = (320, 180)
FPS = 60

PLAYER1_SHIFT = 180
PLAYER2_SHIFT = 40

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
