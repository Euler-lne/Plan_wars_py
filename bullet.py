import pygame
import math
from const import *

class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('./images/bullet1.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class BulletVertical(Bullet):

    def __init__(self, x, y,is_up):
        super().__init__(x, y)
        self.is_up = is_up
        self.damage = 20

    def update(self):
        if self.is_up:
            self.rect.y -= 5
            if self.rect.y <= 0:
                self.kill()
        else:
            self.rect.y += 5
            if self.rect.y >= HEIGHT:
                self.kill()


class BulletNormal(Bullet):

    def __init__(self, x, y, angle):
        super().__init__(x, y)
        self.angle = angle

    def update(self):
        self.rect.y += math.cos(self.angle) * 5
        self.rect.x += math.sin(self.angle) * 5
        if self.rect.y >= HEIGHT or self.rect.y <= 0:
            self.kill()
        if self.rect.x <= 0 or self.rect.x >= WIGHT:
            self.kill()
