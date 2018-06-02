import pygame as pg
from constans import display_width, red, black, display_height
import numpy as np
import time


PROJECTILE = pg.image.load('res\\sprites\\enemy_pro.png')


class Boss:
    def __init__(self, x, y, nr):
        self.parts = []

        self.nr = nr
        self.x = x
        self.y = y
        self.rect = pg.Rect(x, y, 10, 10)
        self.live = 2
        self.gun = np.random.random_integers(0, 60)
        if self.gun == 0:
            self.color = black
            self.threat = np.random.random_integers(300, 400)
        else:
            self.color = red
            self.threat = -100

    def draw(self, game_display):
        for part in self.parts:
            pg.draw.rect(game_display, part.color, part.rect)

    def update(self, blow_sound, pl_pro, boss_por, pew_sound):
        for part in self.parts:
            if part.rect.y < 250 - (part.nr * 10): part.rect.y += 1
            if part.threat > 0: part.threat -= 1
            if part.live <= 0:
                self.parts.remove(part)
                blow_sound[np.random.random_integers(0, 5)].play()
                return part.rect.x + part.rect.width / 2, part.y + part.rect.height / 2
            if -50 < part.threat <= 0 and part.gun == 0:
                part.shot(part, boss_por, pew_sound)

            for projectile in pl_pro.projectiles_left:
                rect = pg.Rect(projectile.x, projectile.y, 10, 10)
                if rect.colliderect(part.rect):
                    pl_pro.remove_off_screen(part.rect)
                    part.live -= 1
            for projectile in pl_pro.projectiles_right:
                rect = pg.Rect(projectile.x, projectile.y, 10, 10)
                if rect.colliderect(part.rect):
                    pl_pro.remove_off_screen(part.rect)
                    part.live -= 1

    @staticmethod
    def shot(part, boss_por, pew_sound):
        part.threat = np.random.random_integers(300, 400)
        boss_por.add_projectile(part.rect.x, part.rect.y)
        pew_sound.play()

    def create_boss(self, sleep):
        time.sleep(sleep)
        for width in range(int(display_width/10)):
            for height in range(20):
                self.parts.append(Boss(width * 10, (height * 10) - 300, len(self.parts) % 20))
        return


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