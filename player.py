import pygame as pg
from constans import display_height, display_width, white
import constans

PLAYER_UP_DOWN = pg.image.load('res\\sprites\\player_up_down.png')
PLAYER_LEFT = pg.image.load('res\\sprites\\player_left.png')
PLAYER_RIGHT = pg.image.load('res\\sprites\\player_right.png')
PLAYER_BLINK = pg.image.load('res\\sprites\\player_blink.png')
PLAYER = [PLAYER_UP_DOWN, PLAYER_BLINK]


class Player(pg.sprite.Sprite):
    def __init__(self, image, lives, score, current_level=None):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.level = current_level
        self.movement_x = 0
        self.movement_y = 0
        self.lives = lives
        self.score = score
        self.is_dead = False
        self.temp = lives - 1
        self.count = 0
        self.blinking = False
        self.spawn = False

    def draw(self, game_display):
        game_display.blit(self.image, self.rect)
        for i in range(0, self.lives):
            game_display.blit(pg.transform.scale(PLAYER_UP_DOWN, (int(65*0.5), int(100*0.5))), (5+(i*65*0.5), 50))

    def update(self, enemies):
        self.bounds()
        self.rect.x += self.movement_x
        self.rect.y += self.movement_y

        if self.movement_x > 0: self.image = PLAYER_RIGHT
        if self.movement_x < 0: self.image = PLAYER_LEFT
        if self.blinking: self.blink()

        if self.lives == 0 or self.score < -500:
            self.is_dead = True
            self.level = 1
        self.level_progress(enemies)
        self.player_hit()

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT: self.turn_left()
            if event.key == pg.K_RIGHT: self.turn_right()
            if event.key == pg.K_UP: self.turn_up()
            if event.key == pg.K_DOWN: self.turn_down()
        elif event.type == pg.KEYUP:
            if event.key == pg.K_LEFT and self.movement_x < 0: self.stop_x()
            if event.key == pg.K_RIGHT and self.movement_x > 0: self.stop_x()
            if event.key == pg.K_DOWN and self.movement_y > 0: self.stop_y()
            if event.key == pg.K_UP and self.movement_y < 0: self.stop_y()

    def bounds(self):
        if self.rect.x + 65 > display_width:
            self.stop_x()
            self.rect.x -= 1
            self.image = PLAYER_UP_DOWN
        if self.rect.x < 0:
            self.stop_x()
            self.rect.x += 1
            self.image = PLAYER_UP_DOWN
        if self.rect.y < 0:
            self.stop_y()
            self.rect.y += 1
            self.image = PLAYER_UP_DOWN
        if self.rect.y + 100 > display_height:
            self.stop_y()
            self.rect.y -= 1
            self.image = PLAYER_UP_DOWN

    def level_progress(self, enemies):
        if 2000 >= self.score >= 1000 and self.level == 1: self.level_up()
        elif 4000 >= self.score >= 2000 and self.level == 2: self.level_up()
        elif 8000 >= self.score >= 4000 and self.level == 3: self.level_up()
        elif self.score >= 8000 and self.level == 4: self.level_up()
        elif enemies.level_up:
            self.level_up()
            self.spawn = True
            enemies.pos_y = 0
            enemies.pos_x = 0

        if len(enemies.enemies) < 50 and self.spawn:
            enemies.add_enemy()
        else:
            self.spawn = False

    def level_up(self):
        constans.comets_size_difficulty += 1
        constans.comet_difficulty_speed += 1
        if self.level > 3 and constans.thret > 430:
            constans.thret -= 400
        elif self.level > 3 and constans.thret > 50:
            constans.thret -= 20
        self.level += 1

    def player_hit(self):
        if self.lives == self.temp:
            self.temp -= 1
            self.blinking = True

    def blink(self):
        if self.count < 3: self.image = PLAYER[1]
        elif self.count < 6: self.image = PLAYER[0]
        elif self.count < 9: self.image = PLAYER[1]
        elif self.count < 12: self.image = PLAYER[0]
        elif self.count < 15: self.image = PLAYER[1]
        elif self.count < 18: self.image = PLAYER[0]
        elif self.count < 21: self.image = PLAYER[1]
        elif self.count < 24: self.image = PLAYER[0]
        if self.count >= 24:
            self.count = 0
            self.blinking = False
        else: self.count += 1

    def stop_x(self):
        self.movement_x = 0
        self.image = PLAYER_UP_DOWN

    def stop_y(self):
        self.movement_y = 0
        self.image = PLAYER_UP_DOWN

    def set_score(self, score): self.score += score

    def turn_left(self): self.movement_x = -6

    def turn_right(self): self.movement_x = 6

    def turn_up(self): self.movement_y = -6

    def turn_down(self): self.movement_y = 6


def draw_points(points, font, game_display):
    text_surf = font.render(str('{0:16}').format(points), True, white)
    text_rect = text_surf.get_rect()
    text_rect.center = (25, 25)
    game_display.blit(text_surf, text_rect)
