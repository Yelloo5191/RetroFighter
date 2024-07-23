import pygame
from util.spritesheet import spritesheet
from enum import Enum

from settings.config import DISPLAY_SIZE, Player_Input_1, Player_Input_2, get_shift

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
        LEFT_PUNCH_JUMP = 9
        RIGHT_PUNCH_JUMP = 10
        LEFT_JUMP_KICK = 11
        RIGHT_JUMP_KICK = 12
        HIT = 13

    def __init__(self, x, y, width, height, image, side, healthbar, debug=False, frozen=False):
        super().__init__()
        self.spritesheet = spritesheet(image)
        self.spritesheet_original = image
        self.hitbox_offset = 0
        self.healthbar = healthbar
        self.health = 100
        self.shift_value = 0
        if side == "right":
            self.spritesheet.flip()
            self.shift_value = get_shift("player 1")
            self.spritesheet.hue_shift(get_shift("player 1"))
            self.hitbox_offset = -1
        if side == "left":
            self.shift_value = get_shift("player 2")
            self.spritesheet.hue_shift(get_shift("player 2"))
            self.hitbox_offset = 1
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
        self.cooldown = 0

        self.frozen = frozen
        self.debug = debug

        self.setup_input()

        hitbox_def = {
            "LEFT_PUNCH": pygame.Rect(20, 30, 25, 20),
            "RIGHT_PUNCH": pygame.Rect(25, 30, 25, 20),
            "LEFT_KICK": pygame.Rect(20, 40, 30, 30),
            "RIGHT_KICK": pygame.Rect(25, 0, 30, 30),
        }

        self.hitboxes = {}

        for name, hitbox in hitbox_def.items():
            hitbox.center = (self.collide_rect.centerx + hitbox.x * self.hitbox_offset, self.collide_rect.centery - hitbox.y // 2)
            self.hitboxes[name] = hitbox
    
    def set_enemy(self, enemy):
        self.enemy = enemy

    def setup_input(self):
        if self.side == "right":
            self.Input = Player_Input_1
        else:
            self.Input = Player_Input_2

    def load_images(self):
        self.images = self.spritesheet.load_all_images((0, 0, 64, 96), (0, 0), (384, 384), colorkey=(0, 0, 0))
        self.images = [pygame.transform.scale(image, (self.width, self.height)) for image in self.images]

        self.animations = {
            "IDLE": self.images[:3],
            "CROUCH": self.images[3:5],
            "RIGHT_PUNCH": self.images[5:8],
            "LEFT_PUNCH": self.images[8:11],
            "LEFT_KICK": self.images[11:14],
            "RIGHT_KICK": self.images[14:17],
            "LEFT_PUNCH_JUMP": self.images[14:17],
            "RIGHT_PUNCH_JUMP": self.images[15:17],
            "LEFT_JUMP_KICK": self.images[17:19],
            "RIGHT_JUMP_KICK": self.images[19:21],
            "HIT": self.images[17:21]
        }
        # print(self.animations)

    def update(self, dt):

        if self.cooldown > 0:
            self.cooldown -= dt

        self.animate(dt)
        if self.frozen:
            return
        self.handle_input()
        self.process_input(dt)
        self.update_state(dt)
    
    def refresh_shift(self):
        player1_shift = get_shift("player 1")
        player2_shift = get_shift("player 2")
        # print(player1_shift, self.shift_value)

        if self.side == "right" and player1_shift != self.shift_value:
            self.spritesheet = spritesheet(self.spritesheet_original)
            self.spritesheet.flip()
            self.spritesheet.hue_shift(player1_shift)
            self.load_images()
        if self.side == "left" and player2_shift != self.shift_value:
            self.spritesheet = spritesheet(self.spritesheet_original)
            self.spritesheet.hue_shift(player2_shift)
            self.load_images()

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
        elif keys[self.Input.ATTACK_3.value]:
            self.current_input = self.Input.ATTACK_3
        elif keys[self.Input.ATTACK_4.value]:
            self.current_input = self.Input.ATTACK_4

    def process_input(self, dt):
        if self.state_time > 0:
            self.state_time -= dt
            return

        if self.input_queue and self.current_input == self.input_queue[-1]:
            return
        
        self.velocity_y += self.gravity * dt
        self.collide_rect.y += self.velocity_y * dt

        # Check if character has landed
        if self.collide_rect.bottom >= DISPLAY_SIZE[0] // 2:  # Assuming 500 is the ground level
            self.collide_rect.bottom = DISPLAY_SIZE[0] // 2
            self.is_jumping = False
            self.velocity_y = 0
            # print(self.collide_rect.y)
        
        if self.is_jumping:
            # if self.current_input == self.Input.ATTACK_1:
            #     self.attack("LEFT_PUNCH")
            pass
        else:
            if (self.state == self.State.IDLE or self.state == self.State.CROUCH or self.state == self.State.JUMP) and not self.cooldown > 0 and not self.state == self.State.HIT:
                
                if self.current_input == self.Input.MOVE_LEFT:
                    self.collide_rect.x -= self.speed * dt
                    for hitbox in self.hitboxes.values():
                        hitbox.x -= self.speed * dt
                    self.state = self.State.MOVE_BACKWARD
                elif self.current_input == self.Input.MOVE_RIGHT:
                    for hitbox in self.hitboxes.values():
                        hitbox.x += self.speed * dt
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
                elif self.current_input == self.Input.ATTACK_3:
                    self.attack("LEFT_KICK")
                elif self.current_input == self.Input.ATTACK_4:
                    self.attack("RIGHT_KICK")
        

        if self.state_time <= 0:
            if self.current_input != self.Input.CROUCH:
                self.state = self.State.IDLE

        self.rect.center = self.collide_rect.center

    def update_state(self, dt):
        pass

    def attack(self, attack_type):
        if self.is_jumping:
            if attack_type == "LEFT_PUNCH":
                self.state = self.State.LEFT_PUNCH_JUMP
                self.state_time = 0.3
        else:
            if attack_type == "LEFT_PUNCH":
                self.state = self.State.LEFT_PUNCH
                self.state_time = 0.3  # Duration of the punch animation
                self.cooldown = 0.6
            elif attack_type == "RIGHT_PUNCH":
                self.state = self.State.RIGHT_PUNCH
                self.state_time = 0.3  # Duration of the punch animation
                self.cooldown = 0.6
            elif attack_type == "LEFT_KICK":
                self.state = self.State.LEFT_KICK
                self.state_time = 0.4
                self.cooldown = 0.7
            elif attack_type == "RIGHT_KICK":
                self.state = self.State.RIGHT_KICK
                self.state_time = 0.4
                self.cooldown = 0.7
        
        if self.hitboxes.get(attack_type):
            # check if hitbox collides with enemy
            if self.hitboxes[attack_type].colliderect(self.enemy.collide_rect):
                self.enemy.healthbar.decrease(10)
                self.enemy.hit()
                print("HIT")

    def hit(self):
        self.state = self.State.HIT
        self.state_time = 0.5
        self.cooldown = 0.5
        self.health -= 10

    def animate(self, dt):
        if self.state == self.State.LEFT_PUNCH:
            self.image = self.animations["LEFT_PUNCH"][int(self.frame) % len(self.animations["LEFT_PUNCH"])]
        elif self.state == self.State.RIGHT_PUNCH:
            self.image = self.animations["RIGHT_PUNCH"][int(self.frame) % len(self.animations["RIGHT_PUNCH"])]
        elif self.state == self.State.LEFT_KICK:
            self.image = self.animations["LEFT_KICK"][int(self.frame) % len(self.animations["LEFT_KICK"])]
        elif self.state == self.State.RIGHT_KICK:
            self.image = self.animations["RIGHT_KICK"][int(self.frame) % len(self.animations["RIGHT_KICK"])]
        elif self.state == self.State.CROUCH:
            if self.frame >= len(self.animations["CROUCH"]) - 1:
                self.frame = len(self.animations["CROUCH"]) - 1
            self.image = self.animations["CROUCH"][int(self.frame)]
        elif self.state == self.State.HIT:
            self.image = self.animations["HIT"][int(self.frame) % len(self.animations["HIT"])]
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
            # render hitboxes
            for name, hitbox in self.hitboxes.items():
                if self.state.name in name:
                    pygame.draw.rect(screen, (0, 255, 0), hitbox, 2)
        
            # draw dot at center of collide_rect
            pygame.draw.circle(screen, (255, 0, 0), self.collide_rect.center, 2)