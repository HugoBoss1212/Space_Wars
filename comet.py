import pygame as pg
import numpy as np
from constans import display_width, display_height, comet_difficulty_speed, comets_size_difficulty, green, base
import time as t
import _thread

COMET_SMALL = pg.image.load('res\\sprites\\rocks_small.png')
COMET_MEDIUM_01 = pg.image.load('res\\sprites\\rocks_medium_01.png')
COMET_MEDIUM_02 = pg.image.load('res\\sprites\\rocks_medium_02.png')
COMET_MEDIUM_03 = pg.image.load('res\\sprites\\rocks_medium_03.png')
COMET_BIG = pg.image.load('res\\sprites\\rocks_big.png')
COMET_MEDIUM = [COMET_MEDIUM_01, COMET_MEDIUM_02, COMET_MEDIUM_03]


class Comet:
    def __init__(self):
        self.comets = []

        self.x = np.random.random_integers(1, display_width - 100)
        self.y = np.random.random_integers(-250, -60)
        self.width = np.random.random_integers(20, 100)
        self.height = np.random.random_integers(40, 100)
        self.angle = np.random.random_integers(-90, 90)
        self.base_health = 0
        if (self.height*self.width) > 8000:
            self.speed = np.random.random_integers(1, 2 + comet_difficulty_speed)
            self.image = pg.transform.rotate(COMET_BIG, self.angle)
            self.live = 6
            self.id = 3
        elif (self.height*self.width) < 2000:
            self.speed = np.random.random_integers(7, 8 + comet_difficulty_speed)
            self.image = pg.transform.rotate(COMET_SMALL, self.angle)
            self.live = 1
            self.id = 1
        else:
            self.speed = np.random.random_integers(4, 5 + comet_difficulty_speed)
            self.image = pg.transform.rotate(np.random.choice(COMET_MEDIUM), self.angle)
            self.live = 3
            self.id = 2
        self.rect = self.image.get_rect()
        self.rect.width *= 0.25
        self.rect.height *= 0.25
        self.rect.x = self.x
        self.size = comets_size_difficulty

    def update(self, rect, pl, po, so, explosions):
        if self.base_health < 0: self.base_health = 0
        if pl.level == 8:
            _thread.start_new_thread(self.add_comets, (5, ))
            pl.level += 1
        explode_sound = explosions[np.random.random_integers(0, 5)]
        for comet in self.comets:
            comet.y += comet.speed
            comet.rect.y = comet.y
            comet.size = comets_size_difficulty
            if self.collide(rect, comet):
                self.comets.remove(comet)
                if pl.level <= 2:
                    self.comets.append(Comet())
                elif pl.level >= 8:
                    self.comets.append(Comet())
                explode_sound.play()
                pl.lives -= 1
                pl.set_score(-20 * pl.lives * comet.live)
                return comet.x + comet.width / 2, comet.y + comet.height / 2
            if comet.y > display_height + 30:
                self.comets.remove(comet)
                if pl.level <= 2:
                    self.comets.append(Comet())
                elif pl.level >= 8:
                    self.comets.append(Comet())
                self.base_health += display_height / base
                if self.base_health >= display_height:
                    pl.is_dead = True
                pl.set_score(-10 * pl.lives)
            if po.remove_off_screen(comet.rect):
                if comet.speed > 1:
                    comet.speed -= 0.5
                if comet.is_dead():
                    try:
                        self.comets.remove(comet)
                    except ValueError:
                        pass
                    if pl.level <= 2:
                        self.comets.append(Comet())
                    elif pl.level >= 8:
                        self.comets.append(Comet())
                    explode_sound.play()
                    pl.set_score(30 * pl.lives)
                    if comet.id is not 1:
                        so.add_scraps(comet.speed, comet.x, comet.y, comet.id)
                        so.add_scraps(comet.speed, comet.x, comet.y, comet.id)
                        so.add_scraps(comet.speed, comet.x, comet.y, comet.id)
                    return comet.x + comet.width / 2, comet.y + comet.height / 2
        return None

    def draw(self, game_display):
        pg.draw.rect(game_display, green, (display_width - 20, self.base_health, 20, display_height))
        for comet in self.comets:
            game_display.blit(pg.transform.scale(comet.image, (int(comet.rect.width), int(comet.rect.height))),
                                                (comet.x, comet.y))

    def is_dead(self):
        self.live -= 1
        if self.live == 0:
            return True
        else:
            return False

    def add_comets(self, sleep, value=np.random.random_integers(1, 2)):
        t.sleep(sleep)
        for i in range(0, value): self.comets.append(Comet())

    @staticmethod
    def collide(rect, comet):
        if comet.rect.colliderect(rect):
            return True
        else:
            return False
