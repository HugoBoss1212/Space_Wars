import pygame as pg
from constans import game_display, display_width, display_height, black, white
import constans


class Menu:
    def __init__(self):
        self.game_display = game_display
        self.menu_loop = True
        self.count = 0
        self.message = [" ", "PRESS ENTER TO START"]
        self.choice = 1

    def __str__(self):
        return "menu loop: " + str(self.menu_loop) + "\tcount: " + str(self.count) + "\tmessage: " +\
               str(self.message[self.choice])

    def update(self):
        self.blink()

    def draw(self, font, font_small):
        game_display.fill(white)
        if constans.to_win == 0:
            text_surf = [font.render("YOU WIN", True, black),
                         font_small.render(str(constans.score), True, black)]
            text_rect = [text_surf[0].get_rect(), text_surf[1].get_rect()]
            text_rect[0].center = (display_width / 2, display_height / 2)
            text_rect[1].center = (display_width / 2, display_height / 2 + 64)
            self.game_display.blit(text_surf[0], text_rect[0])
            self.game_display.blit(text_surf[1], text_rect[1])
        else:
            text_surf = [font.render(self.message[self.choice], True, black),
                         font_small.render("to quit press esc", True, black),
                         font.render("GAME OVER", True, black)]
            text_rect = [text_surf[0].get_rect(), text_surf[1].get_rect(), text_surf[2].get_rect()]
            text_rect[0].center = (display_width / 2, display_height / 2)
            text_rect[1].center = (display_width / 2, display_height / 2 + 64)
            text_rect[2].center = (display_width / 2, display_height / 2 - 128)
            self.game_display.blit(text_surf[0], text_rect[0])
            self.game_display.blit(text_surf[1], text_rect[1])
            if constans.player_dead:
                constans.to_win = 1
                self.game_display.blit(text_surf[2], text_rect[2])

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.menu_loop = False
            if event.key == pg.K_ESCAPE or event.type == pg.QUIT:
                quit()

    def blink(self):
        if self.count % 15 == 0: self.choice_change()
        self.count += 1

    def choice_change(self):
        if self.choice == 1: self.choice = 0
        else: self.choice = 1
