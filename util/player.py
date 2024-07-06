import pygame
from util.spritesheet import spritesheet
from enum import Enum

class Player(pygame.sprite.Sprite):

    class State(Enum):
        IDLE = 0
        WALK = 1
        ATTACK = 2
        JUMP = 3
        FALL = 4
        HURT = 5
        DEAD = 6
    
    class Input(Enum):
        K_a = pygame.K_a
        K_d = pygame.K_d
        K_w = pygame.K_w
        K_s = pygame.K_s
        K_RIGHT = pygame.K_RIGHT
        K_LEFT = pygame.K_LEFT
        K_UP = pygame.K_UP
        K_DOWN = pygame.K_DOWN

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
        self.images = self.spritesheet.load_all_images((0, 0, 64, 96), (0, 0), (192, 192), colorkey=(0, 0, 0))
        self.images = [pygame.transform.scale(image, (self.width, self.height)) for image in self.images]

        self.animations = {
            "IDLE": self.images[:3],
            "ATTACK": self.images[3:6],
            "PUNCH_LEFT": self.images[6:9],
            "KICK_RIGHT": self.images[9:12], 
            "KICK_LEFT": self.images[12:15],
        }
        print(self.animations)
    
    def update(self, dt):
        keys = pygame.key.get_pressed()
        new_input = None

        if keys[self.Input.K_a.value]:
            new_input = self.Input.K_a.value
        elif keys[self.Input.K_d.value]:
            new_input = self.Input.K_d.value
        elif keys[self.Input.K_w.value]:
            new_input = self.Input.K_w.value
        elif keys[self.Input.K_s.value]:
            new_input = self.Input.K_s.value
        elif keys[self.Input.K_RIGHT.value]:
            new_input = self.Input.K_RIGHT.value
        elif keys[self.Input.K_LEFT.value]:
            new_input = self.Input.K_LEFT.value
        elif keys[self.Input.K_UP.value]:
            new_input = self.Input.K_UP.value
        elif keys[self.Input.K_DOWN.value]:
            new_input = self.Input.K_DOWN.value

        if new_input and (not self.input_list or self.input_list[-1] != new_input):
            self.input_list.append(new_input)

        if self.input_list:
            current_input = self.input_list[-1]

            if current_input == self.Input.K_a.value:
                self.rect.x -= self.speed * dt
                self.state = self.State.WALK
            elif current_input == self.Input.K_d.value:
                self.rect.x += self.speed * dt
                self.state = self.State.WALK
            elif current_input == self.Input.K_w.value:
                self.state = self.State.JUMP
            elif current_input == self.Input.K_s.value:
                self.state = self.State.CROUCH
            elif current_input == self.Input.K_RIGHT.value:
                self.state = self.State.ATTACK
                self.attack("PUNCH_RIGHT")
            elif current_input == self.Input.K_LEFT.value:
                self.state = self.State.ATTACK
                self.attack("PUNCH_LEFT")
            elif current_input == self.Input.K_UP.value:
                self.state = self.State.ATTACK
                self.attack("KICK_RIGHT")
            elif current_input == self.Input.K_DOWN.value:
                self.state = self.State.ATTACK
                self.attack("KICK_LEFT")
            else:
                self.state = self.State.IDLE
        else:
            self.state = self.State.IDLE

        # Animation
        self.frame_time -= dt
        if self.frame_time <= 0:
            self.frame_time = 0.15
            animation = self.animations.get(self.state.name, self.animations["IDLE"])
            if self.frame + 1 >= len(animation):
                self.frame = 0
                if self.state.name in self.attack_data:
                    self.state = self.State.IDLE
            else:
                self.frame += 1
            self.image = animation[self.frame]

    def attack(self, attack_type):
        # Add logic for handling the attack
        pass
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
