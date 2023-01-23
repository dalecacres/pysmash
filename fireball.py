import pygame
from spritesheet import SpriteSheet
from projectiles import Projectile

class Fireball(Projectile):
    """
    Class for Mario character
    """

    def __init__(self, direction, pos):
        """
        Creates Player object with Mario's attributes

        Room for expansion with custom functions/attacks
        """
        pygame.init()
        self.tick = {
            'fireball': 0,
            'small_fireball': 0
        }
        self.animation = None

        self.spritesheet = SpriteSheet("resources/mario_sheet.png")
        right = pygame.transform.scale(
            self.spritesheet.image_at((552, 2527, 17, 17), (47, 54, 153)), (50, 76)
        )
        left = pygame.transform.flip(right, flip_x=True, flip_y=False)


        self.animate = {
            "fire_left": self.fireball_l,
            "fire_right": self.fireball_r
        }

        self.images = {
            "left": left,
            "right": right,
        }
        super().__init__(direction, pos)

        self.name = "fireball"
        self.weight = 5
        self.hurtbox = pygame.Rect(self.rect.x, self.rect.y, 50, 76)
        self.speed = 2.5

    def fireball_l(self):
        if self.animation != "neutral_b":
            self.animation = "neutral_b"
        return pygame.transform.flip(self.fireball_r(), flip_x=True, flip_y=False)

    def fireball_r(self):
        if self.animation != "neutral_b":
            self.animation = "neutral_b"
            self.tick['fireball'] = 0
            self.tick['small_fireball'] = 0
        self.tick['small_fireball'] = self.tick['small_fireball'] + 1
        self.tick['fireball'] = (self.tick['fireball'] + 1) % 60
        if self.tick['small_fireball'] < 60:
            tick = self.tick['small_fireball'] // 20
            frames = 6
            x = 483 - tick * frames - 2
            y = 1482
            height = frames
        else:
            self.tick['fireball'] = self.tick['fireball'] % 40
            tick = self.tick['fireball'] // 10
            x = 412
            y = 1446
            frames = 18
            y = y + tick % 2 * frames
            x = x + tick // 2 * frames
            height = 16
        return pygame.transform.scale(
            self.spritesheet.image_at((x, y, frames, height), (47, 54, 153)), (32, 32)
        )