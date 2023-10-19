import pygame
import random
from const import *


class Item(pygame.sprite.Sprite):

    def __init__(self, infect, image_name, rate=1):
        super().__init__()
        self.infect = infect
        image = pygame.image.load(image_name)
        self.image = pygame.transform.scale(
            image, (image.get_width() * rate, image.get_height() * rate))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(self.rect.width, WIGHT - self.rect.width)

    def update(self):
        self.rect.y += 1
        if self.rect.y >= HEIGHT:
            self.kill()
