import os.path

from pygame import *

import pyganim

MOVE_SPEED = 7
WIDTH = 22
HEIGHT = 32
COLOR = '#888888'

JUMP_POWER = 10
GRAVITY = 0.35

ANIMATION_DELAY = 0.1
BASE_DIR = os.path.dirname(__file__) # Полный путь к каталогу с файлами

ANIMATION_RIGHT = [
    (fr'{BASE_DIR}/mario/r1.png'),
    (fr'{BASE_DIR}/mario/r2.png'),
    (fr'{BASE_DIR}/mario/r3.png'),
    (fr'{BASE_DIR}/mario/r4.png'),
    (fr'{BASE_DIR}/mario/r5.png')
]

ANIMATION_LEFT = [
    (fr'{BASE_DIR}/mario/l1.png'),
    (fr'{BASE_DIR}/mario/l2.png'),
    (fr'{BASE_DIR}/mario/l3.png'),
    (fr'{BASE_DIR}/mario/l4.png'),
    (fr'{BASE_DIR}/mario/l5.png')
]

ANIMATION_JUMP_LEFT = [(fr'{BASE_DIR}/mario/jl.png', 0.1)]
ANIMATION_JUMP_RIGHT = [(fr'{BASE_DIR}/mario/jr.png', 0.1)]

ANIMATION_JUMP = [(fr'{BASE_DIR}/mario/j.png', 0.1)]
ANIMATION_STAY = [(fr'{BASE_DIR}/mario/0.png', 0.1)]

class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.x_vel = 0
        self.start_x = x

        self.y_vel = 0
        self.start_y = y

        self.on_ground = False

        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.image.set_colorkey(Color(COLOR)) # Прозрачный фон

        """Анимация движения вправо"""
        bolt_anim = []
        for animation in ANIMATION_RIGHT:
            bolt_anim.append((animation, ANIMATION_DELAY))
        self.bolt_anim_right = pyganim.PygAnimation(bolt_anim)
        self.bolt_anim_right.play()

        """Анимация движения влево"""
        bolt_anim = []
        for animation in ANIMATION_LEFT:
            bolt_anim.append((animation, ANIMATION_DELAY))
        self.bolt_anim_left = pyganim.PygAnimation(bolt_anim)
        self.bolt_anim_left.play()

        """Анимация неподвижности"""
        self.bolt_anim_stay = pyganim.PygAnimation(ANIMATION_STAY)
        self.bolt_anim_stay.play()
        self.bolt_anim_stay.blit(self.image, (0, 0)) # Стоим по умолчанию

        """Анимация прыжка влево"""
        self.bolt_anim_jump_left = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.bolt_anim_jump_left.play()

        """Анимация прыжка вправо"""
        self.bolt_anim_jump_right = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.bolt_anim_jump_right.play()

        """Анимация прыжка вверх"""
        self.bolt_anim_jump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.bolt_anim_jump.play()

    def update(self, left, right, up, platforms):
        if up:
            if self.on_ground:
                self.y_vel = -JUMP_POWER
            self.image.fill(Color(COLOR))
            self.bolt_anim_jump.blit(self.image, (0, 0))
        if left:
            self.x_vel = -MOVE_SPEED
            self.image.fill(Color(COLOR))
            if up:
                self.bolt_anim_jump_left.blit(self.image, (0, 0))
            else:
                self.bolt_anim_left.blit(self.image, (0, 0))

        if right:
            self.x_vel = MOVE_SPEED
            self.image.fill(Color(COLOR))
            if up:
                self.bolt_anim_jump_right.blit(self.image, (0, 0))
            else:
                self.bolt_anim_right.blit(self.image, (0, 0))

        if not (left or right):
            self.x_vel = 0
            if not up:
                self.image.fill(Color(COLOR))
                self.bolt_anim_stay.blit(self.image, (0, 0))

        if not self.on_ground:
            self.y_vel += GRAVITY

        self.on_ground = False
        self.rect.y += self.y_vel
        self.collide(0, self.y_vel, platforms)

        self.rect.x += self.x_vel
        self.collide(self.x_vel, 0, platforms)

    def collide(self, x_vel, y_vel, platforms):
        for platform in platforms:
            if sprite.collide_rect(self, platform):
                if x_vel > 0:
                    self.rect.right = platform.rect.left
                if x_vel < 0:
                    self.rect.left = platform.rect.right

                if y_vel > 0:
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                    self.y_vel = 0

                if y_vel < 0:
                    self.rect.top = platform.rect.bottom
                    self.y_vel = 0