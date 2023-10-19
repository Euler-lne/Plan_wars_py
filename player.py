import pygame
from const import *


class Player(pygame.sprite.Sprite):

    def __init__(self, image_name):
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.rect.x = WIGHT / 2
        self.rect.y = HEIGHT * 3 / 4
        self.speed = 3
        self.sheild1 = Sheild(self, './images/shield01.png')
        self.sheild2 = Sheild(self, './images/shield02.png')
        self.is_sheild = False
        self.is_invi = False

    def update(self, val_move):
        self.rect.x += val_move[0]
        self.rect.y += val_move[1]
        if self.rect.centerx >= WIGHT:
            self.rect.centerx = WIGHT
        elif self.rect.centerx <= 0:
            self.rect.centerx = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        elif self.rect.top <= 0:
            self.rect.top = 0

        self.sheild1.update()
        self.sheild2.update()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.is_invi:
            screen.blit(self.sheild2.image, self.sheild2.rect)
        if self.is_sheild:
            screen.blit(self.sheild1.image, self.sheild1.rect)
            # 自动获取的护盾优先级更高

    def move(self, event):
        val_move = [0, 0]
        if event[pygame.K_LEFT] or event[pygame.K_a]:
            val_move[0] += -1 * self.speed
        if event[pygame.K_RIGHT] or event[pygame.K_d]:
            val_move[0] += 1 * self.speed
        if event[pygame.K_UP] or event[pygame.K_w]:
            val_move[1] += -1 * self.speed
        if event[pygame.K_DOWN] or event[pygame.K_s]:
            val_move[1] += 1 * self.speed
        return val_move


class Sheild(pygame.sprite.Sprite):

    def __init__(self, parent, name):
        self.image = pygame.image.load(name)
        self.rect = self.image.get_rect()
        self.parent = parent.rect
        self.rect.x = self.parent.x - 25
        self.rect.y = self.parent.y - 10

    def update(self):
        self.rect.x = self.parent.x - 25
        self.rect.y = self.parent.y - 10