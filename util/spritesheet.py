import pygame
import colorsys

class spritesheet(object):
    def __init__(self, filename):
        self.flipped = False
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as message:
            print('Unable to load spritesheet image:', filename)
            raise (SystemExit, message)

    def flip(self):
        self.flipped = not self.flipped

    def hue_shift(self, shift):
        for x in range(self.sheet.get_width()):
            for y in range(self.sheet.get_height()):
                color = self.sheet.get_at((x, y))
                h, s, v = colorsys.rgb_to_hsv(color[0] / 255, color[1] / 255, color[2] / 255)
                h = (h * 360 + shift) % 360
                r, g, b = colorsys.hsv_to_rgb(h / 360, s, v)
                self.sheet.set_at((x, y), (r * 255, g * 255, b * 255))

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        if self.flipped:
            image = pygame.transform.flip(image, True, False)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

    def load_all_images(self, rect, top_left, bottom_right, colorkey = None):
        "Loads all images in a spritesheet"
        images = []
        for y in range(top_left[1], bottom_right[1], rect[3]):
            for x in range(top_left[0], bottom_right[0], rect[2]):
                images.append(self.image_at((x, y, rect[2], rect[3]), colorkey))
        return images
