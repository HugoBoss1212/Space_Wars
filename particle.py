import numpy as np
import pygame as pg
from constans import dis_WIDTH, dis_HEIGHT, size

TAIL = pg.image.load('res\\sprites\\tail.png')
TAIL_DIM = pg.image.load('res\\sprites\\taildim.png')
TAIL_DIMMER = pg.image.load('res\\sprites\\taildimer.png')


class Particle:
    def __init__(self):
        self.particles = []
        self.x = np.random.random_integers(1, dis_WIDTH)
        self.y = np.random.random_integers(-120, -60)
        self.tail = np.random.random_integers(70, 100)
        self.speed = np.random.random_integers(2, 7)
        self.size = size

        if self.speed == 2:
            self.image = TAIL_DIMMER
        elif self.speed == 3:
            self.image = TAIL_DIM
        else:
            self.image = TAIL

    def update(self, level):
        for particle in self.particles:
            particle.y += particle.speed + level

            if particle.y > dis_HEIGHT:
                self.particles.remove(particle)
                self.particles.append(Particle())

    def draw(self, game_display):
        for particle in self.particles:
            game_display.blit(particle.image, (particle.x, particle.y))

    def add_particles(self):
        for i in range(0, self.size): self.particles.append(Particle())
