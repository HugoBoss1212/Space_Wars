import math

import numpy as np
import pygame as pg

from constans import display_height, display_width
import constans

ENEMY = pg.image.load('res\\sprites\\enemy.png')
PROJECTILE = pg.image.load('res\\sprites\\enemy_pro.png')
ENEMY_SCRAP_01 = pg.image.load('res\\sprites\\enemy_scrap_01.png')
ENEMY_SCRAP_02 = pg.image.load('res\\sprites\\enemy_scrap_02.png')
ENEMY_SCRAP_03 = pg.image.load('res\\sprites\\enemy_scrap_03.png')
ENEMY_SCRAP_04 = pg.image.load('res\\sprites\\enemy_scrap_04.png')
ENEMY_SCRAP_05 = pg.image.load('res\\sprites\\enemy_scrap_05.png')
ENEMY_SCRAPS_SET_01 = [ENEMY_SCRAP_01, ENEMY_SCRAP_02]
ENEMY_SCRAPS_SET_02 = [ENEMY_SCRAP_03, ENEMY_SCRAP_04, ENEMY_SCRAP_05]


class Enemies:
    def __init__(self):
        super().__init__()
        self.enemies = []
        self.pos_x = 0
        self.pos_y = 0
        self.projectile = Projectiles()
        self.level_up = False

    def draw(self, game_display):
        for enemy in self.enemies: enemy.draw(game_display)

    def update(self, projectile, po, pl, pew_enemy_sound, hurts, explosions, scraps):
        if len(self.enemies) <= 0 and pl.level > 3:
            self.level_up = True
        else:
            self.level_up = False
        for enemy in self.enemies:
            enemy.update(projectile, pew_enemy_sound)
            if enemy.collide(po, hurts, explosions, scraps):
                try:
                    self.enemies.remove(enemy)
                    pl.set_score(100)
                except ValueError:
                    pass

    def add_enemy(self):
        # --------------- ENEMY SPAWN POS ####
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
        self.live = 3
        self.nr = nr
        self.count = 0
        self.threat = np.random.random_integers(100, constans.thret)
        if self.threat <= 20: self.idle = 1
        else: self.idle = 0

    def draw(self, game_display): game_display.blit(self.image, self.rect)

    def update(self, projectile, pew_enemy_sound, po=None, pl=None, hurts=None, explosions=None, scraps=None):

        # ----------- ENEMY PATH 01 ####
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
        # ------------------------ ####

        self.count += 1
        self.threat -= 1
        self.rect.y += self.idle

        if self.threat <= 50: self.idle = np.random.random_integers(-1, 1)
        else: self.idle = 0

        if self.threat <= 5:
            self.threat = np.random.random_integers(100, constans.thret)
            self.idle = 0
            projectile.add_projectile(self.rect.x, self.rect.y)
            pew_enemy_sound.play()

    def collide(self, po, hurts, explosions, scraps):
        for projectile in po.projectiles_left:
            rect = pg.Rect(projectile.x, projectile.y, 10, 10)
            if rect.colliderect(self.rect):
                po.remove_off_screen(self.rect)
                self.live -= 1
        for projectile in po.projectiles_right:
            rect = pg.Rect(projectile.x, projectile.y, 10, 10)
            if rect.colliderect(self.rect):
                po.remove_off_screen(self.rect)
                self.live -= 1
                hurts[np.random.random_integers(0, 2)].play()
        if self.live <= 0:
            explosions[np.random.random_integers(0, 5)].play()
            self.spawn_scraps(scraps)
            return True
        return False

    def spawn_scraps(self, scraps):
        scraps.add_scraps(2, self.rect.x, self.rect.y, np.random.random_integers(2, 3))


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


class Scraps:
    def __init__(self, speed, x, y, value):
        super().__init__()
        self.scraps_list = []

        self.y = y
        self.x = x
        self.speed_x = np.random.uniform(-1.5, 1.5) * speed
        self.speed_y = -(2*speed + math.fabs(self.speed_x))
        self.angle = math.atan((self.speed_x-self.speed_y)/1+(self.speed_x*self.speed_y))*180/math.pi
        if value == 2:
            self.image = pg.transform.rotate(ENEMY_SCRAPS_SET_01[np.random.random_integers(0, 1)], self.angle)
        else:
            self.image = pg.transform.rotate(ENEMY_SCRAPS_SET_02[np.random.random_integers(0, 2)], self.angle)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        for scrap in self.scraps_list:
            scrap.x += scrap.speed_x
            scrap.y += scrap.speed_y

            if scrap.rect.y < 0:
                self.scraps_list.remove(scrap)

    def draw(self, game_display):
        for scrap in self.scraps_list:
            game_display.blit(scrap.image, (scrap.x, scrap.y))

    def add_scraps(self, speed, x, y, value):
        for i in range(value):
            self.scraps_list.append(Scraps(speed, x, y, value))
