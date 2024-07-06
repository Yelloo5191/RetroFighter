class Environment():
    def __init__(self, image, groundHeight):
        self.image = image
        self.groundHeight = groundHeight

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
