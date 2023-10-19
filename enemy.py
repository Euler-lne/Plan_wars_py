import pygame
import random
import bullet
from const import *


class Enemy(pygame.sprite.Sprite):

    def __init__(self, image_name):
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(self.rect.width, WIGHT - self.rect.width)
        self.health = 10
        self.start_bullet_time = pygame.time.get_ticks()
        self.cur_bullet_time = self.start_bullet_time
        self.bullet_time = 1500
        self.can_fire = True
        self.exp = 0

    def takeDamage(self, damage):
        self.health -= damage
        pass

    def move(self):
        pass

    def fire(self):
        pass

    def update(self):
        self.cur_bullet_time = pygame.time.get_ticks()
        if self.cur_bullet_time - self.start_bullet_time >= self.bullet_time and self.can_fire:
            self.fire()
            self.cur_bullet_time = pygame.time.get_ticks()
            self.start_bullet_time = self.cur_bullet_time
        self.move()


class EnemyNormal(Enemy):

    def __init__(self, image_name):
        super().__init__(image_name)
        self.speed = 2
        self.health = 20
        self.exp = 25
        self.id = 1

    def move(self):
        self.rect.y += self.speed
        if self.rect.y >= HEIGHT:
            self.health = 0


class EnemyMiddle(Enemy):

    def __init__(self, image_name, screen):
        super().__init__(image_name)
        self.screen = screen
        self.speed = 1
        self.health = 300
        self.is_right = random.random() >= 0.5
        self.bullet_group = pygame.sprite.Group()
        self.exp = 50
        self.id = 2

    def move(self):
        if self.health <= 100:
            self.rect.y += self.speed
            self.can_fire = False
        elif self.health <= 200 and self.health > 100:
            self.speed = 2
        else:
            if self.is_right:
                self.rect.x += self.speed
            else:
                self.rect.x -= self.speed
            if self.rect.centerx >= WIGHT:
                self.is_right = False
            elif self.rect.centerx <= 0:
                self.is_right = True
        self.bullet_group.update()
        self.bullet_group.draw(self.screen)

        if self.rect.y >= HEIGHT:
            self.health = 0

    def fire(self):
        if self.health > 10:
            new_bullet = bullet.BulletVertical(self.rect.centerx, self.rect.bottom,
                                            False)
            self.bullet_group.add(new_bullet)


class EnemyFinal(EnemyMiddle):

    def __init__(self, image_name, screen):
        super().__init__(image_name, screen)
        self.speed = 1
        self.health = 500
        self.is_right = random.random() >= 0.5
        self.bullet_group = pygame.sprite.Group()
        self.is_down = random.random() >= 0.5
        self.is_right = random.random() >= 0.5
        self.exp = 100
        self.id = 3

    def move(self):
        if self.health <= 300:
            self.speed = 2
        if self.health <= 200:
            self.bullet_time = 750
        if self.rect.centerx >= WIGHT:
            self.is_right = False
        elif self.rect.centerx <= 0:
            self.is_right = True
        if self.rect.bottom >= HEIGHT * 2 / 3:
            self.is_down = False
        elif self.rect.top <= 0:
            self.is_down = True

        if self.is_right:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
        if self.is_down:
            self.rect.y += self.speed
        else:
            self.rect.y -= self.speed

        self.bullet_group.update()
        self.bullet_group.draw(self.screen)

        if self.rect.y >= HEIGHT:
            self.health = 0


    def fire(self):
        new_bullet = bullet.BulletNormal(self.rect.centerx - 10,
                                         self.rect.bottom, -45)
        self.bullet_group.add(new_bullet)
        new_bullet = bullet.BulletNormal(self.rect.centerx + 10,
                                         self.rect.bottom, 45)
        self.bullet_group.add(new_bullet)
