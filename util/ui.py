import pygame
from pygame import font

class Button():
    def __init__(self, x, y, width, height, text, action):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.center = (x, y)
        self.text = text
        self.action = action
        self.font = font.Font(None, 16)
        self.color = (255, 255, 255)
        self.highlighted = False

    def draw(self, screen):
        # Define the points for the slanted sides
        points = [
            (self.x - self.width // 2, self.y - self.height // 2),  # Top-left
            (self.x + self.width // 2 - 10, self.y - self.height // 2),  # Top-right slanted inwards
            (self.x + self.width // 2, self.y + self.height // 2),  # Bottom-right
            (self.x - self.width // 2 + 10, self.y + self.height // 2)  # Bottom-left slanted inwards
        ]
        
        if self.highlighted:
            pygame.draw.polygon(screen, (255, 255, 0), points, 2)
            pygame.draw.polygon(screen, (40, 40, 40), points)
        else:
            pygame.draw.polygon(screen, (100, 45, 90), points)

        text = self.font.render(self.text, True, self.color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
    
    def update(self, mouse_pos):
        # Check if the mouse is within the polygon area
        self.highlighted = self.rect.collidepoint(mouse_pos)
        
        if self.highlighted:
            if pygame.mouse.get_pressed()[0]:
                self.click()
    
    def click(self):
        self.action()
