
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

import _thread

import pygame as pg

import comet
import enemy
import level_transition as lt
import main
import menu
import particle
import player as pl
import projectiles
import scraps
import sparcles_effect as se
from constans import game_display, black, display_width, display_height, \
    white, gravity, start_lives, start_score, fps

pg.mixer.pre_init(44100, -16, 2, 1024)
pg.init()
pg.mixer.init()
pg.display.set_caption('Space Wars')
clock = pg.time.Clock()
player_dead = False
pg.mixer.music.load('res\\music\\MyVeryOwnDeadShip.ogg')
FONT = pg.font.Font('res\\fonts\\Computerfont.ttf', 62)
FONT_SMALL = pg.font.Font('res\\fonts\\Computerfont.ttf', 32)
PEW_SOUND = pg.mixer.Sound('res\\sounds\\pew.wav')
PEW_ENEMY_SOUND = pg.mixer.Sound('res\\sounds\\pew_enemy.wav')
EXPLOSION_01 = pg.mixer.Sound('res\\sounds\\exp_01.wav')
EXPLOSION_02 = pg.mixer.Sound('res\\sounds\\exp_02.wav')
EXPLOSION_03 = pg.mixer.Sound('res\\sounds\\exp_03.wav')
EXPLOSION_04 = pg.mixer.Sound('res\\sounds\\exp_04.wav')
EXPLOSION_05 = pg.mixer.Sound('res\\sounds\\exp_05.wav')
EXPLOSION_06 = pg.mixer.Sound('res\\sounds\\exp_06.wav')
EXPLOSIONS = [EXPLOSION_01, EXPLOSION_02, EXPLOSION_03, EXPLOSION_04, EXPLOSION_05, EXPLOSION_06]
HURT_ENEMY_01 = pg.mixer.Sound('res\\sounds\\hurt_enemy01.wav')
HURT_ENEMY_02 = pg.mixer.Sound('res\\sounds\\hurt_enemy02.wav')
HURT_ENEMY_03 = pg.mixer.Sound('res\\sounds\\hurt_enemy03.wav')
HURTS = [HURT_ENEMY_01, HURT_ENEMY_02, HURT_ENEMY_03]


def game_loop():
    menu_object = menu.Menu()
    # ----------- INIT MENU ####
    while menu_object.menu_loop:
        menu_object.update()
        menu_object.draw(FONT, FONT_SMALL)
        for event in pg.event.get():
            menu_object.get_event(event)
        pg.display.update()
        clock.tick(fps)

    # ----------- INIT ####
    pg.mixer.music.play(-1)
    player = pl.Player(pl.PLAYER_UP_DOWN, start_lives, start_score, 1)
    player.rect.center = display_width * 0.5 - 33, display_height * 0.8
    enemies = enemy.Enemies()
    enemies_pro = enemy.Projectiles()
    projectiles_objects = projectiles.Projectiles()
    particles_objects = particle.Particle()
    particles_objects.add_particles()
    comets_objects = comet.Comet()
    _thread.start_new_thread(comets_objects.add_comets, (10, ))
    level_transition = lt.LevelTransition(0, -400, game_display, white, 3, FONT, display_width, display_height + 400)
    scraps_objects = scraps.Scraps(0, 0, 0, 0)
    scraps_objects_enemies = enemy.Scraps(0, 0, 0, 0)
    particles = []
    sparkles = []
    exit_ = False

    while not player.is_dead:
        main.player_dead = True

        # ----------- HANDLING EVENTS ####
        for event in pg.event.get():
            if event.type == pg.QUIT:
                player.is_dead = True
                exit_ = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    exit_ = True
                    player.is_dead = True
            if event.type == pg.KEYUP:
                pass
            player.get_event(event)
            projectiles_objects.get_event(event, player.rect, PEW_SOUND, particles, sparkles)

        # ----------- UPDATES ####
        # ----------- ENEMY SPAWN INIT ####
        if player.level == 3 and len(enemies.enemies) < 50:
            enemies.add_enemy()
        elif player.level == 3:
            player.level += 1

        projectiles_objects.update()
        particles_objects.update(player.level)
        comet_pos = comets_objects.update(pg.Rect(player.rect.x + 10, player.rect.y, 45, 85),
                                          player, projectiles_objects, scraps_objects, EXPLOSIONS)
        if comet_pos is not None:
            for i in range(3):
                particles.append(se.ParticleBall(game_display, comet_pos, (0, -1), gravity, particles, sparkles, 20))
        enemies.update(enemies_pro, projectiles_objects, player, PEW_ENEMY_SOUND, HURTS, EXPLOSIONS,
                       scraps_objects_enemies)
        enemies_pro.update(player)
        scraps_objects_enemies.update()
        player.update(enemies)
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
        enemies.draw(game_display)
        scraps_objects_enemies.draw(game_display)
        player.draw(game_display)
        pl.draw_points(player.score, FONT_SMALL, game_display)
        scraps_objects.draw(game_display)
        for p in particles: p.draw()
        for s in sparkles: s.draw()
        enemies_pro.draw(game_display)
        level_transition.update(player.level)

        pg.display.update()
        clock.tick(fps)

    if not exit_:
        game_loop()


game_loop()
pg.quit()
quit()
