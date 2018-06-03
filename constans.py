import pygame as pg
import os

display_width = 1024
display_height = 1080
size = 100
black = (0, 0, 0)
white = (255, 255, 255)
red = (179, 0, 0,)
red_gun = (255, 0, 0)
green = (0, 166, 81)
blue = (0, 0, 255)
comet_difficulty_speed = 0
comets_size_difficulty = 3
os.environ['SDL_VIDEO_WINDOW_POS'] = "300,0"
game_display = pg.display.set_mode((display_width, display_height), pg.NOFRAME)
gravity = (0, -.1)
start_lives = 4
start_score = 50
score = 0
fps = 60
base = 10
thret = 3000
player_dead = False
to_win = 0
