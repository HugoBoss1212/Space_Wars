import math
import random
from vec2d import Vec2d
import pygame as pg


class Particle(object):
    def __init__(self, surface, pos, vel, gravity, container, age, color='red'):
        self.age = age
        self.surface = surface
        self.pos = Vec2d(pos)
        vel = [vel[0]+random.uniform(-3, 3), vel[1]+random.uniform(-3, 3)]
        self.vel = Vec2d(vel)
        if self.vel.length > 10:
            self.vel.length = 10
        self.gravity = Vec2d(gravity)
        self.container = container
        self.color = pg.Color(color)

        self.radius = random.randint(4, 16)
        self.connect_dist = self.radius * 4
        self.surf_size = surface.get_size()
        self.drag = .9
        self.connections = []

    def update(self):
        self.connections = []
        self.vel = (self.vel + self.gravity) * self.drag
        self.pos = self.pos + self.vel
        if self.out_of_bounds():
            self.container.remove(self)

    def draw(self):
        pass

    def out_of_bounds(self):
        out_of_bounds = False
        if self.pos[0] < -self.radius or self.pos[0] > self.surf_size[0] + self.radius:
            out_of_bounds = True
        elif self.pos[1] < -self.radius or self.pos[1] > self.surf_size[1] + self.radius:
            out_of_bounds = True
        return out_of_bounds


class ParticleBall(Particle):
    def __init__(self, surface, pos, vel, gravity, container, sparkle_container, age=20, color='red'):
        super(ParticleBall, self).__init__(surface, pos, vel, gravity, container, age, color)

        self.sparkle_container = sparkle_container
        self.connections = []
        self.created_sparkles = []

    def draw(self):
        for p in self.container:
            if p is not self:
                if self not in p.connections:
                    dist = math.sqrt(abs(pow(p.pos.x-self.pos.x, 2) + pow(p.pos.y-self.pos.y, 2)))
                    if dist < self.connect_dist:
                        self.connections.append(p)
                        self.create_sparkles(p)

    def create_sparkles(self, target):
        if target not in self.created_sparkles:
            for r in range(self.radius):
                self.sparkle_container.append(ParticleSparkle(self.surface, (self.pos.x, self.pos.y),
                                                              (self.vel.x, self.vel.y),
                                                              self.gravity, self.sparkle_container, self.age))
            self.created_sparkles.append(target)


class ParticleSparkle(Particle):
    def __init__(self, surface, pos, vel, gravity, container, age=20, color='white'):
        super(ParticleSparkle, self).__init__(surface, pos, vel, gravity, container, age, color)
        self.value_step = 100.0/float(self.age)

    def update(self):
        super(ParticleSparkle, self).update()
        hsva = self.color.hsva
        value = hsva[2]
        alpha = hsva[3]
        value -= self.value_step
        alpha -= self.value_step
        if value < 0 or alpha < 0:
            try:
                self.container.remove(self)
            except ValueError:
                pass
        else:
            self.color.hsva = (int(hsva[0]), int(hsva[1]), value, alpha)

    def draw(self):
        pg.draw.line(self.surface, self.color, (self.pos[0], self.pos[1]), (self.pos[0], self.pos[1]))
