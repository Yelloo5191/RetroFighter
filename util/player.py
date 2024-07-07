import pygame
from util.spritesheet import spritesheet
from enum import Enum

class Player(pygame.sprite.Sprite):

    class State(Enum):
        IDLE = 0
        WALK = 1
        CROUCH = 2
        JUMP = 3
        ATTACK = 4
        FALL = 5
        HURT = 6
        DEAD = 7
    
    class Input(Enum):
        MOVE_LEFT = pygame.K_a
        MOVE_RIGHT = pygame.K_d
        JUMP = pygame.K_w
        CROUCH = pygame.K_s
        RIGHT = pygame.K_RIGHT
        LEFT = pygame.K_LEFT
        UP = pygame.K_UP
        DOWN = pygame.K_DOWN

    def __init__(self, x, y, width, height, image):
        super().__init__()
        self.spritesheet = spritesheet(image)
        self.image = self.spritesheet.image_at((0, 0, 64, 96), colorkey=(0, 0, 0))
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = width
        self.height = height
        self.speed = 250
        self.load_images()
        self.frame = 0
        self.frame_time = 0.15
        self.state = self.State.IDLE

        self.input_list = []
        self.animation_in_progress = False

        self.attack_data = {
            "PUNCH_RIGHT": {
                "damage": 10,
                "range": 50,
                "speed": 100,
                "cooldown": 0.5,
                "duration": 0.2,
            },
            "PUNCH_LEFT": {
                "damage": 10,
                "range": 50,
                "speed": 100,
                "cooldown": 0.5,
                "duration": 0.2,
            },
            "KICK_RIGHT": {
                "damage": 15,
                "range": 50,
                "speed": 100,
                "cooldown": 0.5,
                "duration": 0.2,
            },
            "KICK_LEFT": {
                "damage": 15,
                "range": 50,
                "speed": 100,
                "cooldown": 0.5,
                "duration": 0.2,
            },
        }
    
    def load_images(self):
        self.images = self.spritesheet.load_all_images((0, 0, 64, 96), (0, 0), (304, 192), colorkey=(0, 0, 0))
        self.images = [pygame.transform.scale(image, (self.width, self.height)) for image in self.images]

        self.animations = {
            "IDLE": self.images[:3],
            "ATTACK": self.images[3:6],
            "CROUCH": self.images[7:8],
        }
        print(self.animations)
    
    def update(self, dt):
        keys = pygame.key.get_pressed()
        new_input = None

        if keys[self.Input.MOVE_LEFT.value]:
            new_input = self.Input.MOVE_LEFT.value
        elif keys[self.Input.MOVE_RIGHT.value]:
            new_input = self.Input.MOVE_RIGHT.value
        elif keys[self.Input.JUMP.value]:
            new_input = self.Input.JUMP.value
        elif keys[self.Input.CROUCH.value]:
            new_input = self.Input.CROUCH.value
        elif keys[self.Input.RIGHT.value]:
            new_input = self.Input.RIGHT.value
        elif keys[self.Input.LEFT.value]:
            new_input = self.Input.LEFT.value
        elif keys[self.Input.UP.value]:
            new_input = self.Input.UP.value
        elif keys[self.Input.DOWN.value]:
            new_input = self.Input.DOWN.value

        if new_input and (not self.input_list or self.input_list[-1] != new_input):
            self.input_list.append(new_input)
        else:
            self.input_list.append("*")

        if self.input_list:
            current_input = self.input_list[-1]

            if current_input == self.Input.MOVE_LEFT.value:
                self.rect.x -= self.speed * dt
                self.state = self.State.WALK
            elif current_input == self.Input.MOVE_RIGHT.value:
                self.rect.x += self.speed * dt
                self.state = self.State.WALK
            elif current_input == self.Input.JUMP.value:
                self.state = self.State.JUMP
            elif current_input == self.Input.CROUCH.value:
                self.state = self.State.CROUCH
            elif current_input == self.Input.RIGHT.value:
                self.state = self.State.ATTACK
                self.attack("PUNCH_RIGHT")
            elif current_input == self.Input.LEFT.value:
                self.state = self.State.ATTACK
                self.attack("PUNCH_LEFT")
            elif current_input == self.Input.UP.value:
                self.state = self.State.ATTACK
                self.attack("KICK_RIGHT")
            elif current_input == self.Input.DOWN.value:
                self.state = self.State.ATTACK
                self.attack("KICK_LEFT")
            else:
                self.state = self.State.IDLE
        else:
            self.state = self.State.IDLE
        # print(self.state.name)
        # Animation
        self.frame_time -= dt
        if self.frame_time <= 0:
            self.frame_time = 0.15
            animation = self.animations.get(self.state.name, self.animations["IDLE"])
            if self.frame + 1 >= len(animation):
                self.frame = 0
                if self.state.name in self.attack_data:
                    self.state = self.State.IDLE
                    self.animation_in_progress = False
            else:
                self.frame += 1
            self.image = animation[self.frame]

    def attack(self, attack_type):
        # Add logic for handling the attack
        self.animation_in_progress = True
        # Add any additional logic required for attack
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
