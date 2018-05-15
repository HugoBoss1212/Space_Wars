import pygame as pg


PROJECTILE = pg.image.load('res\\sprites\\projectal.png')


class Projectiles:
    def __init__(self):
        self.projectiles_left = []
        self.projectiles_right = []

    def update(self):
        for projectile in self.projectiles_left: projectile.update()
        for projectile in self.projectiles_right: projectile.update()
        self.remove_off_screen()

    def draw(self, game_display):
        for projectile in self.projectiles_left: projectile.draw(game_display)
        for projectile in self.projectiles_right: projectile.draw(game_display)

    def get_event(self, event, pl_rect):
        if event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                self.projectiles_left.append(Projectile(pl_rect.x, pl_rect.y))
                self.projectiles_right.append(Projectile(pl_rect.x + 32, pl_rect.y))

    def remove_off_screen(self, rect=None):
        for projectile in self.projectiles_left:
            if projectile.remove(projectile, rect):
                self.projectiles_left.remove(projectile)
                if rect is not None:
                    return True
        for projectile in self.projectiles_right:
            if projectile.remove(projectile, rect):
                self.projectiles_right.remove(projectile)
                if rect is not None:
                    return True


class Projectile(Projectiles):
    def __init__(self, x_player, y_player):
        super().__init__()
        self.x = x_player + 10
        self.y = y_player + 30
        self.speed = 10
        self.image = PROJECTILE
        self.rect = self.image.get_rect()

    def draw(self, game_display):
        game_display.blit(self.image, (self.x, self.y))

    def remove(self, projectile, rect=None):
        if projectile.y < -10:
            return True
        elif rect is not None:
            if rect.colliderect(pg.Rect(self.x, self.y, 10, 10)):
                return True
        else:
            return False

    def update(self):
        self.y -= self.speed
