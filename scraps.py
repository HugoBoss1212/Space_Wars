import pygame as pg
import numpy as np
from constans import dis_WIDTH, dis_HEIGHT

SCRAP_MEDIUM = pg.image.load('res\\sprites\\scraps_medium.png')
SCRAP_BIG = pg.image.load('res\\sprites\\scraps_big.png')


class Scraps:
    def __init__(self, speed, x, y, id_):
        self.scraps_list = []

        self.y = y
        self.x = x
        # TODO: Wyliczać kąt obiektu i losować prędkość poruszania sie po osi x
        self.speed_x_y = [(0.3 * speed, 2 * speed), (0, 2 * speed), (-0.3 * speed, 2 * speed)]
        self.direction = np.random.random_integers(0, 2)
        if id_ == 2:
            if self.direction == 0:
                self.image = pg.transform.rotate(SCRAP_BIG, 30)
            if self.direction == 1:
                self.image = SCRAP_BIG
            if self.direction == 2:
                self.image = pg.transform.rotate(SCRAP_BIG, -30)
        elif id_ == 3:
            if self.direction == 0:
                self.image = pg.transform.rotate(SCRAP_MEDIUM, 30)
            if self.direction == 1:
                self.image = SCRAP_MEDIUM
            if self.direction == 2:
                self.image = pg.transform.rotate(SCRAP_MEDIUM, -30)
        else:
            self.image = None
        if self.image is not None:
            self.rect = self.image.get_rect()
            self.rect.width *= 0.35
            self.rect.height *= 0.35
            self.rect.x = self.x
            self.rect.y = self.y

    def update(self, rect, pl, po):
        for scrap in self.scraps_list:
            scrap.x += scrap.speed_x_y[scrap.direction][0]
            scrap.y += scrap.speed_x_y[scrap.direction][1]
            if scrap.x > dis_WIDTH or scrap.x < -scrap.rect.width or scrap.y > dis_HEIGHT:
                self.scraps_list.remove(scrap)
            if scrap.rect.colliderect(rect):
                self.scraps_list.remove(scrap)
                pl.lives -= 1
                pl.set_score(-10 * pl.level)
            if po.remove_off_screen(scrap.rect):
                pl.set_score(10)
                try:
                    self.scraps_list.remove(scrap)
                except ValueError:
                    pass

    def draw(self, game_display):
        for scrap in self.scraps_list:
            game_display.blit(pg.transform.scale(scrap.image, (int(scrap.rect.width), int(scrap.rect.height))),
                              (scrap.x, scrap.y))

    def add_scraps(self, speed, x, y, id_):
        for i in range(id_):
            self.scraps_list.append(Scraps(speed, x, y, id_))
