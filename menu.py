import pygame as pg
from constans import game_display, display_width, display_height, black, white
import constans


FORWARD = pg.image.load('res\\sprites\\back.png')
BACK = pg.image.load('res\\sprites\\forward.png')


class Menu:
    def __init__(self):
        self.game_display = game_display
        self.menu_loop = True
        self.count = 0
        self.message = [" ", "PRESS ENTER TO START"]
        self.choice = 1
        self.help_screen = False
        self.screens = []

    def __str__(self):
        return "menu loop: " + str(self.menu_loop) + "\tcount: " + str(self.count) + "\tmessage: " +\
               str(self.message[self.choice])

    def update(self):
        self.blink()
        for screen in self.screens: screen.update()

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
                         font.render("GAME OVER", True, black),
                         font_small.render("to help press 'H'", True, black)]
            text_rect = [text_surf[0].get_rect(), text_surf[1].get_rect(), text_surf[2].get_rect(),
                         text_surf[3].get_rect()]
            text_rect[0].center = (display_width / 2, display_height / 2)
            text_rect[1].center = (display_width / 2, display_height / 2 + 64)
            text_rect[2].center = (display_width / 2, display_height / 2 - 128)
            text_rect[3].center = (display_width / 2, display_height / 2 + 96)
            self.game_display.blit(text_surf[0], text_rect[0])
            self.game_display.blit(text_surf[1], text_rect[1])
            self.game_display.blit(text_surf[3], text_rect[3])
            if constans.player_dead:
                constans.to_win = 1
                self.game_display.blit(text_surf[2], text_rect[2])
        for screen in self.screens: screen.draw(font, font_small)

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN and not self.help_screen:
                self.menu_loop = False
            if (event.key == pg.K_ESCAPE or event.type == pg.QUIT) and not self.help_screen:
                quit()
            elif event.key == pg.K_ESCAPE:
                self.screens.clear()
                self.help_screen = False
            if event.key == pg.K_h:
                self.help_screen = True
                self.screens.append(HelpScreen())
        for screen in self.screens: screen.get_event(event)

    def blink(self):
        if self.count % 15 == 0: self.choice_change()
        self.count += 1

    def choice_change(self):
        if self.choice == 1: self.choice = 0
        else: self.choice = 1


class HelpScreen(Menu):
    def __init__(self):
        super().__init__()
        self.page = 0

    def draw(self, font, font_small):
        self.game_display.fill(white)
        text_surf = [font_small.render(str(self.page), True, black),
                     font_small.render("press 'esc' to go back", True, black)]
        text_rect = [text_surf[0].get_rect(), text_surf[1].get_rect()]
        text_rect[0].topright = (display_width - 32, 32)
        text_rect[1].topleft = (32, 32)
        self.game_display.blit(text_surf[0], text_rect[0])
        self.game_display.blit(text_surf[1], text_rect[1])
        if self.page == 0:
            self.game_display.blit(FORWARD, (display_width - (32 * 3), 32))
            text_surf = [font_small.render("Welcome to Space Wars !", True, black),
                         font_small.render("The goal of the game is to fight off", True, black),
                         font_small.render("hostile enemies and final boss, when", True, black),
                         font_small.render("protecting your base from comets ", True, black),
                         font_small.render("approaching ahead.", True, black),
                         font_small.render("To do so you are controlling", True, black),
                         font_small.render("space ship 'CRUSIER 01'.", True, black),
                         font_small.render("Controls are arrow keys to move", True, black),
                         font_small.render("spacebar to shoot.", True, black),
                         font_small.render("Good luck !", True, black)]
            text_rect = []
            for rect in text_surf: text_rect.append(rect.get_rect())
            i = 0
            for rect in text_rect:
                rect.center = (display_width / 2, (display_height / 2 + (32 * i)) - 300)
                i += 1
            for j in range(i):
                self.game_display.blit(text_surf[j], text_rect[j])
        elif self.page == 1:
            self.game_display.blit(FORWARD, (display_width - (32 * 3), 32))
            self.game_display.blit(BACK, (display_width - (32 * 4), 32))
        elif self.page == 2:
            self.game_display.blit(FORWARD, (display_width - (32 * 3), 32))
            self.game_display.blit(BACK, (display_width - (32 * 4), 32))
        elif self.page == 3:
            self.game_display.blit(BACK, (display_width - (32 * 4), 32))

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                if self.page < 3: self.page += 1
            if event.key == pg.K_LEFT:
                if self.page > 0: self.page -= 1
