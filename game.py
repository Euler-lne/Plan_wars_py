import pygame
import enemy
import player
import bullet
import random
import item
from const import *

FPS = 60


class Game():

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIGHT, HEIGHT))
        self.bg = pygame.image.load('./images/background.png')
        self.font = pygame.font.Font('./font/font.ttf', 40)
        self.score = 0
        self.life = 3
        self.bullet_num = 1
        self.enemy_num_total = 0
        self.enemy_num_limit = 10
        self.enemy2_total = 0
        self.enemy2_limit = 0
        self.enemy3_total = 0
        self.enemy3_limit = 0
        self.clock = pygame.time.Clock()

        self.start_bullet_time = pygame.time.get_ticks()
        self.start_enemy_time = pygame.time.get_ticks()
        self.start_invi_time = pygame.time.get_ticks()
        self.start_item_time = pygame.time.get_ticks()

        self.player = player.Player('./images/me1.png')
        self.enemy_group = pygame.sprite.Group()  #所有敌人都有
        self.ememy_fire_group = pygame.sprite.Group()  #存放发子弹的敌人
        self.bullet_group = pygame.sprite.Group()
        self.item_group = pygame.sprite.Group()
        self.enemy_time = 2000
        self.bullet_time = 500
        self.item_time = 10000
        self.invi_time = 2000

        self.screen.blit(self.bg, (0, 0))
        self.updateUI()

    def start(self):
        while True:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            key_pressed = pygame.key.get_pressed()
            val_move = self.player.move(key_pressed)
            self.spawnBullet()
            self.spawnEnemies()
            self.spawnItem()
            self.updateGameObject(val_move)
            self.checkCollision()
            self.setDifficut()
            self.updateUI()
            if self.life == 0:
                break
        self.over()

    def updateGameObject(self, val_move):
        self.screen.blit(self.bg, (0, 0))

        self.player.update(val_move)
        self.player.draw(self.screen)
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        self.bullet_group.update()
        self.bullet_group.draw(self.screen)
        self.item_group.update()
        self.item_group.draw(self.screen)

    def updateUI(self):
        score_str = self.font.render('score ' + str(self.score), True,
                                     (0, 0, 0))
        life_str = self.font.render('life ' + str(self.life), True, (0, 0, 0))
        self.screen.blit(score_str, (0, 0))
        self.screen.blit(life_str, (WIGHT - 100, 0))
        pygame.display.update()

    def spawnEnemies(self):
        cur_time = pygame.time.get_ticks()
        if cur_time - self.start_enemy_time >= self.enemy_time and self.enemy_num_total < self.enemy_num_limit:
            if random.random(
            ) >= 0.5 and self.enemy2_total < self.enemy2_limit:
                enemy_middle = enemy.EnemyMiddle("./images/enemy2.png",
                                                 self.screen)
                self.enemy2_total += 1
                self.enemy_group.add(enemy_middle)
                self.ememy_fire_group.add(enemy_middle)
            elif random.random(
            ) >= 0.7 and self.enemy3_total < self.enemy3_limit:
                enemy_final = enemy.EnemyFinal("./images/enemy3_n1.png",
                                               self.screen)
                self.enemy_group.add(enemy_final)
                self.ememy_fire_group.add(enemy_final)
                self.enemy3_total += 1
            else:
                enemy_normal = enemy.EnemyNormal("./images/enemy1.png")
                self.enemy_group.add(enemy_normal)
            self.enemy_num_total += 1
            self.start_enemy_time = pygame.time.get_ticks()

    def spawnBullet(self):
        cur_time = pygame.time.get_ticks()
        if cur_time - self.start_bullet_time >= self.bullet_time:
            x = []
            if self.bullet_num == 1:
                x = [self.player.rect.centerx - 1]
            elif self.bullet_num == 2:
                x = [
                    self.player.rect.centerx - 11, self.player.rect.centerx + 9
                ]
            elif self.bullet_num == 3:
                x = [
                    self.player.rect.centerx - 1,
                    self.player.rect.centerx + 14,
                    self.player.rect.centerx - 16
                ]
            elif self.bullet_num == 4:
                x = [
                    self.player.rect.centerx - 9, self.player.rect.centerx + 7,
                    self.player.rect.centerx - 25,
                    self.player.rect.centerx + 23
                ]
            elif self.bullet_num == 5:
                x = [
                    self.player.rect.centerx - 1,
                    self.player.rect.centerx + 14,
                    self.player.rect.centerx - 16,
                    self.player.rect.centerx + 29,
                    self.player.rect.centerx - 31
                ]
            for _ in x:
                new_bullet = bullet.BulletVertical(_, self.player.rect.top,
                                                   True)
                self.bullet_group.add(new_bullet)
            self.start_bullet_time = pygame.time.get_ticks()

    def spawnItem(self):
        cur_time = pygame.time.get_ticks()
        if cur_time - self.start_item_time >= self.item_time:
            key = random.random()
            if key >= 0.8:
                new_item = item.Item(Infect.HEALTH, './images/life1.png')
                self.item_group.add(new_item)
            elif key >= 0.2 and self.bullet_num < 5 and key <= 0.8:
                new_item = item.Item(Infect.BULLET,
                                     './images/bullet_supply.png')
                self.item_group.add(new_item)
            else:
                new_item = item.Item(Infect.SHEILD, './images/shield01.png',
                                     0.5)
                self.item_group.add(new_item)
            self.start_item_time = pygame.time.get_ticks()

    def checkCollision(self):
        dict_collision = pygame.sprite.groupcollide(self.bullet_group,
                                                    self.enemy_group, True,
                                                    False)
        if dict_collision:
            for key in dict_collision.keys():
                for enemy_ in dict_collision[key]:
                    enemy_.takeDamage(key.damage)
                    if enemy_.health <= 0:
                        self.score += enemy_.exp
                    # 不可以直接dict_collision[key].takeDamage(key.damage)
                    # 因为这个是一个列表
        for sprite in self.enemy_group.sprites():
            if sprite.health <= 0:
                self.updateEnemyNum(sprite)
                sprite.kill()
        items = pygame.sprite.spritecollide(self.player, self.item_group, True)
        for item_ in items:
            if item_.infect == Infect.BULLET:
                if self.bullet_num < 5:
                    self.bullet_num += 1
            elif item_.infect == Infect.BULLET_SPEED:
                pass
            elif item_.infect == Infect.SHEILD:
                self.player.is_sheild = True
            elif item_.infect == Infect.HEALTH:
                self.life += 1
            self.score += 10

        enemy_bullet_group = pygame.sprite.Group()
        for sprite in self.ememy_fire_group.sprites():
            enemy_bullet_group.add(sprite.bullet_group)
        enemy_bullets = pygame.sprite.spritecollide(self.player,
                                                    enemy_bullet_group, True)
        enemies = pygame.sprite.spritecollide(self.player, self.enemy_group,
                                              True)
        for enemy_ in enemies:
            self.updateEnemyNum(enemy_)
        if len(enemy_bullets) > 0 or len(enemies) > 0:
            if self.player.is_invi == False:
                if self.player.is_sheild:
                    self.player.is_sheild = False
                else:
                    self.life -= 1
                    self.player.is_invi = True
                    self.start_invi_time = pygame.time.get_ticks()

        if self.player.is_invi:
            cur_time = pygame.time.get_ticks()
            if cur_time - self.start_invi_time >= self.invi_time:
                self.player.is_invi = False

    def setDifficut(self):
        if self.score >= 5000:
            self.enemy_time = 1000
        elif self.score >= 4000 and self.score < 5000:
            self.enemy2_limit = 5
            self.enemy3_limit = 3
        elif self.score >= 3000 and self.score < 4000:
            self.enemy2_limit = 5
            self.enemy3_limit = 2
        elif self.score >= 2000 and self.score < 3000:
            self.enemy_time = 1250
            self.enemy2_limit = 3
            self.enemy3_limit = 1
        elif self.score >= 1000 and self.score < 2000:
            self.enemy_time = 1500
            self.enemy2_limit = 1
            self.enemy_num_limit = 30
        elif self.score >= 500 and self.score < 1000:
            self.enemy_time = 1750

    def updateEnemyNum(self, sprite):
        if sprite.id == 2:
            self.enemy2_total -= 1
        elif sprite.id == 3:
            self.enemy3_total -= 1
        self.enemy_num_total -= 1

    def over(self):
        while True:
            self.game_over = pygame.image.load('./images/gameover.png')
            self.screen.blit(
                self.game_over,
                (WIGHT / 2 - self.game_over.get_width() / 2, HEIGHT / 2))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.quit()
                        exit()
