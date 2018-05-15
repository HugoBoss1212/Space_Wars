import pygame as pg
from constans import dis_HEIGHT, dis_WIDTH, white
import constans

PLAYER_UP_DOWN = pg.image.load('res\\sprites\\player_up_down.png')
PLAYER_LEFT = pg.image.load('res\\sprites\\player_left.png')
PLAYER_RIGHT = pg.image.load('res\\sprites\\player_right.png')


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

    def draw(self, game_display):
        game_display.blit(self.image, self.rect)
        for i in range(0, self.lives):
            game_display.blit(pg.transform.scale(PLAYER_UP_DOWN, (int(65*0.5), int(100*0.5))), (5+(i*65*0.5), 50))

    def update(self):
        self.bounds()
        self.rect.x += self.movement_x
        self.rect.y += self.movement_y

        if self.movement_x > 0:
            self.image = PLAYER_RIGHT
        if self.movement_x < 0:
            self.image = PLAYER_LEFT

        if self.lives == 0 or self.score < -500:
            self.is_dead = True
            self.level = 1
        self.level_progress()

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT: self.turn_left()
            if event.key == pg.K_RIGHT: self.turn_right()
            if event.key == pg.K_UP: self.turn_up()
            if event.key == pg.K_DOWN: self.turn_down()
        elif event.type == pg.KEYUP:
            if event.key == pg.K_LEFT and self.movement_x < 0:
                self.stop_x()
                self.image = PLAYER_UP_DOWN
            if event.key == pg.K_RIGHT and self.movement_x > 0:
                self.stop_x()
                self.image = PLAYER_UP_DOWN
            if event.key == pg.K_DOWN and self.movement_y > 0:
                self.stop_y()
                self.image = PLAYER_UP_DOWN
            if event.key == pg.K_UP and self.movement_y < 0:
                self.stop_y()
                self.image = PLAYER_UP_DOWN

    def bounds(self):
        if self.rect.x + 65 > dis_WIDTH:
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
        if self.rect.y + 100 > dis_HEIGHT:
            self.stop_y()
            self.rect.y -= 1
            self.image = PLAYER_UP_DOWN

    def level_progress(self):
        if 2000 >= self.score >= 1000 and self.level == 1: self.level_up()
        elif 4000 >= self.score >= 2000 and self.level == 2: self.level_up()
        elif 8000 >= self.score >= 4000 and self.level == 3: self.level_up()
        elif 14000 >= self.score >= 8000 and self.level == 4: self.level_up()
        elif 18000 >= self.score >= 14000 and self.level == 5: self.level_up()
        elif 25000 >= self.score >= 18000 and self.level == 6: self.level_up()
        elif 30000 >= self.score >= 25000 and self.level == 7: self.level_up()
        elif 35000 >= self.score >= 30000 and self.level == 8: self.level_up()

    def level_up(self):
        constans.comets_size_difficulty += 1
        constans.comet_difficulty_speed += 1
        self.level += 1

    def set_score(self, score): self.score += score

    def turn_left(self): self.movement_x = -6

    def turn_right(self): self.movement_x = 6

    def turn_up(self): self.movement_y = -6

    def turn_down(self): self.movement_y = 6

    def stop_x(self): self.movement_x = 0

    def stop_y(self): self.movement_y = 0


def draw_points(points, font, game_display):
    text_surf = font.render(str('{0:16}').format(points), True, white)
    text_rect = text_surf.get_rect()
    text_rect.center = (25, 25)
    game_display.blit(text_surf, text_rect)
