import pygame as pg
from constans import display_height, display_width, thret
import math
import numpy as np

ENEMY = pg.image.load('res\\sprites\\enemy.png')
PROJECTILE = pg.image.load('res\\sprites\\enemy_pro.png')


class Enemies:
    def __init__(self):
        super().__init__()
        self.enemies = []
        self.pos_x = 0
        self.pos_y = 0
        self.projectile = Projectiles()

    def draw(self, game_display):
        for enemy in self.enemies: enemy.draw(game_display)

    def update(self, projectile):
        for enemy in self.enemies: enemy.update(projectile)

    def add_enemy(self):
        self.pos_y += 1
        if len(self.enemies) % 5 == 0:
            self.pos_x += 1
            self.pos_y = 0
        if len(self.enemies) % 25 == 0:
            self.pos_x += 1
        self.enemies.append(Enemy((((display_width - 200) - 25) - (self.pos_x * 50)), -60, self.pos_y))


class Enemy(Enemies):
    def __init__(self, x, y, nr):
        super().__init__()
        self.rect = pg.Rect(x, y, 50, 50)
        self.vel = 4
        self.image = ENEMY
        self.nr = nr
        self.count = 0
        self.threat = np.random.random_integers(100, thret)
        if self.threat <= 20: self.idle = 1
        else: self.idle = 0

    def draw(self, game_display): game_display.blit(self.image, self.rect)

    def update(self, projectile):
        if self.rect.y < display_height / 4 - (self.nr * 50):
            self.rect.y += self.vel
        else:
            if math.fabs(self.vel) != 0 and self.vel > 0: self.vel -= 0.1
            elif math.fabs(self.vel) != 0 and self.vel < 0: self.vel += 0.1
            if self.vel > 0:
                if self.rect.x + self.vel < display_width - (display_width / 8): self.rect.x += self.vel
                else: self.vel *= -1
            else:
                if self.rect.x + self.vel > display_width / 8: self.rect.x += self.vel
                else: self.vel *= -1

        self.count += 1
        self.threat -= 1
        self.rect.y += self.idle

        if self.threat <= 50: self.idle = np.random.random_integers(-1, 1)
        else: self.idle = 0

        if self.threat <= 5:
            self.threat = np.random.random_integers(100, thret)
            self.idle = 0
            projectile.add_projectile(self.rect.x, self.rect.y)


class Projectiles:
    def __init__(self):
        self.projectiles = []

    def update(self, player):
        for projectile in self.projectiles:
            if projectile.update(player):
                self.projectiles.remove(projectile)

    def draw(self, game_display):
        for projectile in self.projectiles: projectile.draw(game_display)

    def add_projectile(self, x, y): self.projectiles.append(Projectile(x, y))


class Projectile(Projectiles):
    def __init__(self, x_player, y_player):
        super().__init__()
        self.x = x_player + 20
        self.y = y_player + 50
        self.speed = 8
        self.image = PROJECTILE
        self.rect = pg.Rect(self.x, self.y, 20, 50)

    def draw(self, game_display):
        game_display.blit(self.image, (self.x, self.y))

    def update(self, player):
        self.rect = pg.Rect(self.x, self.y, 20, 50)
        self.y += self.speed
        if self.y > display_height:
            return True
        if self.collide(self.rect, player.rect):
            player.lives -= 1
            return True
        return False

    @staticmethod
    def collide(rect, comet):
        if comet.colliderect(rect):
            return True
        else:
            return False
