import pygame
from util.spritesheet import spritesheet
from enum import Enum

from settings.config import DISPLAY_SIZE, Player_Input_1, Player_Input_2

class Player(pygame.sprite.Sprite):

    class State(Enum):
        IDLE = 0
        MOVE_FORWARD = 1
        MOVE_BACKWARD = 2
        JUMP = 3
        CROUCH = 4
        LEFT_PUNCH = 5
        RIGHT_PUNCH = 6
        LEFT_KICK = 7
        RIGHT_KICK = 8

    def __init__(self, x, y, width, height, image, side, debug=False):
        super().__init__()
        self.spritesheet = spritesheet(image)
        if side == "right":
            self.spritesheet.flip()
            self.spritesheet.hue_shift(180)
        if side == "left":
            self.spritesheet.hue_shift(40)
        self.image = self.spritesheet.image_at((0, 0, 64, 96), colorkey=(0, 0, 0))
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.collide_rect = pygame.Rect(x, y, width-32, height-16)
        self.width = width
        self.height = height
        self.speed = 250
        self.jump_speed = -400
        self.gravity = 1400
        self.load_images()
        self.frame = 0
        self.frame_time = 0.15
        self.side = side

        self.state = self.State.IDLE
        self.state_time = 0
        self.input_queue = []
        self.velocity_y = 0
        self.is_jumping = False

        self.debug = debug

        self.setup_input()

    def setup_input(self):
        if self.side == "right":
            self.Input = Player_Input_1
        else:
            self.Input = Player_Input_2

    def load_images(self):
        self.images = self.spritesheet.load_all_images((0, 0, 64, 96), (0, 0), (304, 192), colorkey=(0, 0, 0))
        self.images = [pygame.transform.scale(image, (self.width, self.height)) for image in self.images]

        self.animations = {
            "IDLE": self.images[:3],
            "CROUCH": self.images[3:5],
            "LEFT_PUNCH": self.images[5:7],
            "RIGHT_PUNCH": self.images[7:9],
        }
        print(self.animations)

    def update(self, dt):
        self.handle_input()
        self.process_input(dt)
        self.update_state(dt)
        self.animate(dt)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.current_input = None

        if keys[self.Input.MOVE_LEFT.value]:
            self.current_input = self.Input.MOVE_LEFT
        elif keys[self.Input.MOVE_RIGHT.value]:
            self.current_input = self.Input.MOVE_RIGHT
        elif keys[self.Input.JUMP.value]:
            self.current_input = self.Input.JUMP
        elif keys[self.Input.CROUCH.value]:
            self.current_input = self.Input.CROUCH
        elif keys[self.Input.ATTACK_1.value]:
            self.current_input = self.Input.ATTACK_1
        elif keys[self.Input.ATTACK_2.value]:
            self.current_input = self.Input.ATTACK_2

    def process_input(self, dt):
        if self.state_time > 0:
            self.state_time -= dt
            return

        if self.input_queue and self.current_input == self.input_queue[-1]:
            return

        if self.current_input == self.Input.MOVE_LEFT:
            self.collide_rect.x -= self.speed * dt
            self.state = self.State.MOVE_BACKWARD
        elif self.current_input == self.Input.MOVE_RIGHT:
            self.collide_rect.x += self.speed * dt
            self.state = self.State.MOVE_FORWARD
        elif self.current_input == self.Input.JUMP and not self.is_jumping:
            self.velocity_y = self.jump_speed
            self.is_jumping = True
            self.state = self.State.JUMP
        elif self.current_input == self.Input.CROUCH:
            self.state = self.State.CROUCH
        elif self.current_input == self.Input.ATTACK_1:
            self.attack("LEFT_PUNCH")
        elif self.current_input == self.Input.ATTACK_2:
            self.attack("RIGHT_PUNCH")
        if self.is_jumping:
            self.velocity_y += self.gravity * dt
            self.collide_rect.y += self.velocity_y * dt

            # Check if character has landed
            if self.collide_rect.bottom >= DISPLAY_SIZE[0] // 2:  # Assuming 500 is the ground level
                self.collide_rect.bottom = DISPLAY_SIZE[0] // 2
                self.is_jumping = False
                self.velocity_y = 0
                print(self.collide_rect.y)

        if self.state_time <= 0:
            if self.current_input != self.Input.CROUCH:
                self.state = self.State.IDLE

        self.rect.center = self.collide_rect.center

    def update_state(self, dt):
        pass

    def attack(self, attack_type):
        if attack_type == "LEFT_PUNCH":
            self.state = self.State.LEFT_PUNCH
            self.state_time = 0.3  # Duration of the punch animation
        elif attack_type == "RIGHT_PUNCH":
            self.state = self.State.RIGHT_PUNCH
            self.state_time = 0.3  # Duration of the punch animation

    def animate(self, dt):
        if self.state == self.State.LEFT_PUNCH:
            self.image = self.animations["LEFT_PUNCH"][int(self.frame) % len(self.animations["LEFT_PUNCH"])]
        elif self.state == self.State.RIGHT_PUNCH:
            self.image = self.animations["RIGHT_PUNCH"][int(self.frame) % len(self.animations["RIGHT_PUNCH"])]
        elif self.state == self.State.CROUCH:
            if self.frame >= len(self.animations["CROUCH"]) - 1:
                self.frame = len(self.animations["CROUCH"]) - 1
            self.image = self.animations["CROUCH"][int(self.frame)]
        else:
            self.image = self.animations["IDLE"][int(self.frame) % len(self.animations["IDLE"])]
        # print(self.state)

        self.frame += dt / self.frame_time
        if self.frame >= len(self.animations[self.state.name]):
            self.frame = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.debug:
            # render self.rect
            pygame.draw.rect(screen, (255, 0, 0), self.collide_rect, 2)
