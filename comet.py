import pygame as pg
import numpy as np
from constans import dis_WIDTH, dis_HEIGHT, comet_difficulty_speed, comets_size_difficulty
import time as t

COMET_SMALL = pg.image.load('res\\sprites\\rocks_small.png')
COMET_MEDIUM = pg.image.load('res\\sprites\\rocks_medium.png')
COMET_BIG = pg.image.load('res\\sprites\\rocks_big.png')


class Comet:
    def __init__(self):
        self.comets = []

        self.x = np.random.random_integers(1, dis_WIDTH)
        self.y = np.random.random_integers(-250, -60)
        self.width = np.random.random_integers(20, 100)
        self.height = np.random.random_integers(40, 100)
        if (self.height*self.width) > 8000:
            self.speed = np.random.random_integers(1, 2 + comet_difficulty_speed)
            self.image = COMET_BIG
            self.live = 6
            self.id = 3
        elif (self.height*self.width) < 1500:
            self.speed = np.random.random_integers(7, 8 + comet_difficulty_speed)
            self.image = COMET_SMALL
            self.live = 1
            self.id = 1
        else:
            self.speed = np.random.random_integers(4, 5 + comet_difficulty_speed)
            self.image = COMET_MEDIUM
            self.live = 3
            self.id = 2
        self.rect = self.image.get_rect()
        self.rect.width *= 0.25
        self.rect.height *= 0.25
        self.rect.x = self.x
        self.size = comets_size_difficulty

    def update(self, rect, pl, po, so):
        for comet in self.comets:
            comet.y += comet.speed
            comet.rect.y = comet.y
            comet.size = comets_size_difficulty
            if self.collide(rect, comet):
                self.comets.remove(comet)
                self.comets.append(Comet())
                pl.lives -= 1
                pl.set_score(-20 * pl.lives * comet.live)
            if comet.y > dis_HEIGHT + 30:
                self.comets.remove(comet)
                self.comets.append(Comet())
                pl.set_score(-10 * pl.lives)
            if po.remove_off_screen(comet.rect):
                if comet.speed > 1:
                    comet.speed -= 0.5
                if comet.is_dead():
                    try:
                        self.comets.remove(comet)
                    except ValueError:
                        pass
                    self.comets.append(Comet())
                    pl.set_score(30 * pl.lives)
                    if comet.id is not 1:
                        so.add_scraps(comet.speed, comet.x, comet.y, comet.id)
                    return comet.x + comet.width / 2, comet.y + comet.height / 2
        return None

    def draw(self, game_display):
        for comet in self.comets:
            game_display.blit(pg.transform.scale(comet.image, (int(comet.rect.width), int(comet.rect.height))),
                                                (comet.x, comet.y))

    def is_dead(self):
        self.live -= 1
        if self.live == 0:
            return True
        else:
            return False

    def add_comets(self, sleep):
        t.sleep(sleep)
        for i in range(0, self.size): self.comets.append(Comet())

    @staticmethod
    def collide(rect, comet):
        if comet.rect.colliderect(rect):
            return True
        else:
            return False
