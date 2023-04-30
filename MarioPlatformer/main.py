import pygame
from pygame import *

from blocks import PLATFORM_WIDTH, PLATFORM_HEIGHT, Platform
from player import Player

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
DISPLAY = (WINDOW_WIDTH, WINDOW_HEIGHT)
BACKGROUND_COLOR = '#004400'

FPS = 60
CLOCK = pygame.time.Clock()


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WINDOW_WIDTH / 2, -t + WINDOW_HEIGHT / 2 # Центрирование камеры относительно марио

    l = min(0, l) # Не движемся дальше левого края карты
    l = max(-(camera.width - WINDOW_WIDTH), l) # Не движимся дальше правого края
    l = max(-(camera.height - WINDOW_HEIGHT), t) # Не движимся дальше нижней части
    t = min(0, t) # Не движемся дальше верхней части

    return Rect(l, t, w, h)

LEVEL_1 = [
    '-----------------------------------',
    '-                                 -',
    '-          --                     -',
    '-                          ---    -',
    '-            --                   -',
    '-                                 -',
    '-                   -----         -',
    '-                                 -',
    '-         -                --     -',
    '-                                 -',
    '-                 ---             -',
    '-                                 -',
    '-          --                     -',
    '-                   -----         -',
    '-                                 -',
    '-    -------                      -',
    '-                                 -',
    '-----------------------------------',
]




def run_game():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption('Mario')
    bg = Surface(DISPLAY)
    bg.fill(Color(BACKGROUND_COLOR))

    mario = Player(55, 55)
    left = False
    right = False
    up = False

    entities = pygame.sprite.Group()
    platforms = list()

    entities.add(mario)

    total_level_width = len(LEVEL_1[0]) * PLATFORM_WIDTH
    total_level_height = len(LEVEL_1) * PLATFORM_HEIGHT

    camera = Camera(camera_configure, total_level_width, total_level_height)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                raise SystemExit('QUIT')
            """Перемещение по Ох"""
            if event.type == KEYDOWN and event.key == K_LEFT:
                left = True
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                right = True

            if event.type == KEYUP and event.key == K_LEFT:
                left = False
            if event.type == KEYUP and event.key == K_RIGHT:
                right = False
            """Перемещение по Оy"""
            if event.type == KEYDOWN and event.key == K_SPACE:
                up = True
            elif event.type == KEYUP and event.key == K_SPACE:
                up = False

        screen.blit(bg, (0, 0))

        """Отрисовка платформ"""
        x, y = 0, 0
        for row in LEVEL_1:
            for symbol in row:
                if symbol == '-':
                    platform = Platform(x, y)
                    entities.add(platform)
                    platforms.append(platform)
                x += PLATFORM_WIDTH
            y += PLATFORM_HEIGHT
            x = 0

        """Отрисовка персонажа"""
        camera.update(mario)
        mario.update(left, right, up, platforms)
        for ent in entities:
            screen.blit(ent.image, camera.apply(ent))

        CLOCK.tick(FPS)
        pygame.display.update()

if __name__ == '__main__':
    run_game()