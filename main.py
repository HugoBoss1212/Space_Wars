
""" # ----------------------------------------------------------------------------- #
                        Projekt gry opartej na bibliotece pygame
                        Kacper Lechowicz L3
                                             |__
                                             |/
                                             ---
                                             / | [
                                      !      | |||
                                    _/|     _/|-++'
                                +  +--|    |--|--|_ |-
                             { /|__|  |/__|  |--- |||__/
                            +---------------___[}-_===_.'____                   /
                        ____`-' ||___-{]_| _[}-  |     |_[___==--              / _
        __..._____--==/___]_|__|_____________________________[___==--___,-----' .7
        |                                                                   BB-61/
        _______________________________________________________________________|

""" # --------------------------------------------------------------------------- #

import pygame as pg
import particle
import projectiles
import comet
from constans import gameDisplay, black, dis_WIDTH, dis_HEIGHT, white, GRAVITY
import _thread
import player as pl
import level_transition as lt
import scraps
import sparcles_effect as se

pg.init()
pg.display.set_caption('Space Wars')
clock = pg.time.Clock()
FONT = pg.font.Font('res\\fonts\\Computerfont.ttf', 62)
FONT_SMALL = pg.font.Font('res\\fonts\\Computerfont.ttf', 32)


def game_loop():

    # ----------- INIT ####
    player = pl.Player(pl.PLAYER_UP_DOWN, 3, 50, 1)
    player.rect.center = dis_WIDTH * 0.5 - 33, dis_HEIGHT * 0.8
    projectiles_objects = projectiles.Projectiles()
    particles_objects = particle.Particle()
    particles_objects.add_particles()
    comets_objects = comet.Comet()
    _thread.start_new_thread(comets_objects.add_comets, (10, ))
    level_transition = lt.LevelTransition(0, -400, gameDisplay, white, 3, FONT, dis_WIDTH, dis_HEIGHT + 400)
    scraps_objects = scraps.Scraps(0, 0, 0, 0)
    particles = []
    sparkles = []

    while not player.is_dead:

        # ----------- HANDLING EVENTS ####
        for event in pg.event.get():
            if event.type == pg.QUIT:
                player.is_dead = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    particles.append(se.ParticleBall(gameDisplay,
                                                     (player.rect.x + player.rect.width/2, player.rect.y),
                                                     (0, -1), GRAVITY, particles, sparkles, 8))
            if event.type == pg.KEYUP:
                pass
            player.get_event(event)
            projectiles_objects.get_event(event, player.rect)

        # ----------- UPDATES ####
        projectiles_objects.update()
        particles_objects.update(player.level)
        comet_pos = comets_objects.update(pg.Rect(player.rect.x + 10, player.rect.y, 45, 85),
                                          player, projectiles_objects, scraps_objects)
        if comet_pos is not None:
            for i in range(3):
                particles.append(se.ParticleBall(gameDisplay, comet_pos, (0, -1), GRAVITY, particles, sparkles, 20))
        player.update()
        scrap_pos = scraps_objects.update(pg.Rect(player.rect.x + 10, player.rect.y, 45, 85),
                                          player, projectiles_objects)
        if scrap_pos is not None:
            particles.append(se.ParticleBall(gameDisplay, scrap_pos, (0, -1), GRAVITY, particles, sparkles, 8))
        for p in particles:
            p.update()
            if len(particles) > 70:
                particles.remove(p)
        for s in sparkles: s.update()

        # ----------- DRAW ####
        gameDisplay.fill(black)
        projectiles_objects.draw(gameDisplay)
        particles_objects.draw(gameDisplay)
        comets_objects.draw(gameDisplay)
        player.draw(gameDisplay)
        pl.draw_points(player.score, FONT_SMALL, gameDisplay)
        scraps_objects.draw(gameDisplay)
        for p in particles: p.draw()
        for s in sparkles: s.draw()
        level_transition.update(player.level)

        pg.display.update()
        clock.tick(60)

    game_loop()


game_loop()
pg.quit()
quit()
