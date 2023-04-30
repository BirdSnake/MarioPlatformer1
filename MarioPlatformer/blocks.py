from pygame import *
import os


PLATFORM_WIDTH, PLATFORM_HEIGHT = 32, 32
PLATFORM_COLOR = '#FF6262'

class Platform(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load(fr'blocks/platform.png')
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)