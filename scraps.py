import pygame as pg
import numpy as np
from constans import display_width, display_height
import math

SCRAP_MEDIUM_01 = pg.image.load('res\\sprites\\scraps_medium_01.png')
SCRAP_MEDIUM_02 = pg.image.load('res\\sprites\\scraps_medium_02.png')
SCRAP_MEDIUM_03 = pg.image.load('res\\sprites\\scraps_medium_03.png')
SCRAP_MEDIUM_04 = pg.image.load('res\\sprites\\scraps_medium_04.png')
SCRAP_BIG_01 = pg.image.load('res\\sprites\\scraps_big_01.png')
SCRAP_BIG_02 = pg.image.load('res\\sprites\\scraps_big_02.png')
SCRAP_BIG_03 = pg.image.load('res\\sprites\\scraps_big_03.png')
SCRAP_BIG_04 = pg.image.load('res\\sprites\\scraps_big_04.png')
SCRAP_MEDIUM = [SCRAP_MEDIUM_01, SCRAP_MEDIUM_02, SCRAP_MEDIUM_03, SCRAP_MEDIUM_04]
SCRAP_BIG = [SCRAP_BIG_01, SCRAP_BIG_02, SCRAP_BIG_03, SCRAP_BIG_04]
SCRAP = [SCRAP_BIG, SCRAP_MEDIUM]


class Scraps:
    def __init__(self, speed, x, y, id_):
        self.scraps_list = []

        self.y = y
        self.x = x
        self.speed_x = np.random.uniform(-1.5, 1.5) * speed
        self.speed_y = 2*speed - math.fabs(self.speed_x)
        self.angle = math.atan((self.speed_x-self.speed_y)/1+(self.speed_x*self.speed_y))*180/math.pi
        if id_ == 3:
            choice = SCRAP[np.random.random_integers(0, 1)]
            self.image = pg.transform.rotate(np.random.choice(choice), self.angle)
        elif id_ == 2:
            self.image = pg.transform.rotate(np.random.choice(SCRAP_MEDIUM), self.angle)
        else:
            self.image = np.random.choice(SCRAP_MEDIUM)
        self.rect = self.image.get_rect()
        self.rect.width *= 0.3
        self.rect.height *= 0.3
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self, rect, pl, po):
        for scrap in self.scraps_list:
            scrap.x += scrap.speed_x
            scrap.y += scrap.speed_y
            scrap.rect.x = scrap.x
            scrap.rect.y = scrap.y
            if scrap.x > display_width or scrap.x < -scrap.rect.width or scrap.y > display_height:
                self.scraps_list.remove(scrap)
            if scrap.rect.colliderect(rect):
                self.scraps_list.remove(scrap)
                pl.set_score(-10 * pl.level )
            if po.remove_off_screen(scrap.rect):
                pl.set_score(10)
                try:
                    self.scraps_list.remove(scrap)
                except ValueError:
                    pass
                return scrap.x + scrap.rect.width / 2, scrap.y + scrap.rect.height / 2
        return None

    def draw(self, game_display):
        for scrap in self.scraps_list:
            game_display.blit(pg.transform.scale(scrap.image, (int(scrap.rect.width), int(scrap.rect.height))),
                              (scrap.x, scrap.y))

    def add_scraps(self, speed, x, y, id_):
        for i in range(id_):
            self.scraps_list.append(Scraps(speed, x, y, id_))
