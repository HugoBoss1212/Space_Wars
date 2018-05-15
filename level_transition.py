from constans import dis_HEIGHT, black, dis_WIDTH
import pygame as pg


class LevelTransition:
    def __init__(self, x, y, game_display, color, speed, font, width, height):
        self.x = x
        self.y = y
        self.start_y = y
        self.game_display = game_display
        self.color = color
        self.speed = speed
        self.temp = 1
        self.transition = False
        self.font = font
        self.width = width
        self.height = height

    def update(self, level):
        if level == 1 and level == self.temp:
            self.transition = True
            self.temp = level + 1
        elif level > 1 and level == self.temp:
            self.transition = True
            self.temp = level + 1
            self.speed += level/3
            self.height = 200

        if self.transition:
            if self.y < dis_HEIGHT:
                self.y += self.speed
                self.draw(level)
            else:
                self.transition = False
                self.y = self.start_y

    def draw(self, level):
        pg.draw.rect(self.game_display, self.color, (self.x, self.y, self.width, self.height), 0)
        text_surf = self.font.render("battle_hub_0" + str(level), True, black)
        text_rect = text_surf.get_rect()
        text_rect.center = (dis_WIDTH/2, self.y + 100)
        self.game_display.blit(text_surf, text_rect)
