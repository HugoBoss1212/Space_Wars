
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
from constans import game_display, black, display_width, display_height,\
                     white, gravity, start_lives, start_score, fps
import _thread
import player as pl
import level_transition as lt
import scraps
import sparcles_effect as se

pg.mixer.pre_init(44100, -16, 1, 512)
pg.init()
pg.mixer.init()
pg.display.set_caption('Space Wars')
clock = pg.time.Clock()
pg.mixer.music.load('res\\music\\MyVeryOwnDeadShip.ogg')
FONT = pg.font.Font('res\\fonts\\Computerfont.ttf', 62)
FONT_SMALL = pg.font.Font('res\\fonts\\Computerfont.ttf', 32)
PEW_SOUND = pg.mixer.Sound('res\\sounds\\pew.wav')
EXPLOSION_01 = pg.mixer.Sound('res\\sounds\\exp_01.wav')
EXPLOSION_02 = pg.mixer.Sound('res\\sounds\\exp_02.wav')
EXPLOSION_03 = pg.mixer.Sound('res\\sounds\\exp_03.wav')
EXPLOSION_04 = pg.mixer.Sound('res\\sounds\\exp_04.wav')
EXPLOSION_05 = pg.mixer.Sound('res\\sounds\\exp_05.wav')
EXPLOSION_06 = pg.mixer.Sound('res\\sounds\\exp_06.wav')
EXPLOSIONS = [EXPLOSION_01, EXPLOSION_02, EXPLOSION_03, EXPLOSION_04, EXPLOSION_05, EXPLOSION_06]


def game_loop():
    # TODO Press enter to start

    # ----------- INIT ####
    pg.mixer.music.play(-1)
    player = pl.Player(pl.PLAYER_UP_DOWN, start_lives, start_score, 1)
    player.rect.center = display_width * 0.5 - 33, display_height * 0.8
    projectiles_objects = projectiles.Projectiles()
    particles_objects = particle.Particle()
    particles_objects.add_particles()
    comets_objects = comet.Comet()
    _thread.start_new_thread(comets_objects.add_comets, (10, ))
    level_transition = lt.LevelTransition(0, -400, game_display, white, 3, FONT, display_width, display_height + 400)
    scraps_objects = scraps.Scraps(0, 0, 0, 0)
    particles = []
    sparkles = []
    exit_ = False

    while not player.is_dead:

        # ----------- HANDLING EVENTS ####
        for event in pg.event.get():
            if event.type == pg.QUIT:
                player.is_dead = True
                exit_ = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    pass
                if event.key == pg.K_ESCAPE:
                    exit_ = True
                    player.is_dead = True
            if event.type == pg.KEYUP:
                pass
            player.get_event(event)
            projectiles_objects.get_event(event, player.rect, PEW_SOUND, particles, sparkles)

        # ----------- UPDATES ####
        projectiles_objects.update()
        particles_objects.update(player.level)
        comet_pos = comets_objects.update(pg.Rect(player.rect.x + 10, player.rect.y, 45, 85),
                                          player, projectiles_objects, scraps_objects, EXPLOSIONS)
        if comet_pos is not None:
            for i in range(3):
                particles.append(se.ParticleBall(game_display, comet_pos, (0, -1), gravity, particles, sparkles, 20))
        player.update()
        scrap_pos = scraps_objects.update(pg.Rect(player.rect.x + 10, player.rect.y, 45, 85),
                                          player, projectiles_objects)
        if scrap_pos is not None:
            particles.append(se.ParticleBall(game_display, scrap_pos, (0, -1), gravity, particles, sparkles, 12))
        for p in particles:
            p.update()
            try:
                if clock.get_fps() + 1 < fps: particles.remove(p)
            except ValueError:
                pass
        for s in sparkles: s.update()

        # ----------- DRAW ####
        game_display.fill(black)
        projectiles_objects.draw()
        particles_objects.draw(game_display)
        comets_objects.draw(game_display)
        player.draw(game_display)
        pl.draw_points(player.score, FONT_SMALL, game_display)
        scraps_objects.draw(game_display)
        for p in particles: p.draw()
        for s in sparkles: s.draw()
        level_transition.update(player.level)

        pg.display.update()
        clock.tick(fps)

    if not exit_:
        game_loop()


game_loop()
pg.quit()
quit()
