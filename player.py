"""
class doctring
"""
# pylint: disable=unnecessary-pass
import abc
import pygame

vec = pygame.math.Vector2
FRIC = -.25

class Player(abc.ABC, pygame.sprite.Sprite):
    """
    Doctring
    """
    def __init__(self, direction):
        super().__init__()
        self.direction = direction
        self._health = 0
        self.image = self.images[direction]
        self.rect = self.image.get_rect()
        self._stocks = 3

        self.pos = vec((620, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        
        self.jump_count = 0
        self.attacking = 0

    def knockback(self, strength_y, direction):
        """
        Knock a character back based on knockback amount from an attack

        Args:
            strength (int): amount of knockback to apply to the character
        """
        if direction == 'right':
            strength_x = strength_y
        elif direction == 'left':
            strength_x = -strength_y
        self.vel = vec(strength_x, strength_y)

    @abc.abstractmethod
    def attack(self):
        pass

    def gravity(self):
        """
        Apply acceleration due to gravity to player object except if on a
        platform
        """
        self.acc = vec(0,0.5)

        hits = pygame.sprite.spritecollide(self, self.platforms, False)
        if hits:
            self.pos.y = hits[0].rect.top + 1
            self.vel.y = 0
            self.jump_count = 2

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value

    @property
    def stocks(self):
        return self._stocks

    @stocks.setter
    def stocks(self, value):
        self._stocks = value

    def jump(self):
        """
        Make the character jump
        """
        if self.jump_count:
            self.vel.y = -15
            self.jump_count -= 1

    def left(self):
        """
        Move the character left
        """
        self.acc.x = -self.speed
        self.image = self.images['left']
        self.mover = 'walk'
        self.direction = 'left'

    def right(self):
        """
        Move the character right
        """
        self.acc.x = self.speed
        self.image = self.images['right']
        self.mover = 'walk'
        self.direction = 'right'

    def move(self):
        """
        Take the current acceleration and velocity, calculate player's position,
        and update the player's rectangle
        """
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + .5 * self.acc

        self.rect.midbottom = self.pos
        self.set_boxes()
        self.character_image()

        self.is_dead()

    def is_dead(self):
        if not(-400 <= self.pos.x <= 1640) or  not(-400 <= self.pos.y <= 1120):
            self._health = 0
            self._stocks -= 1
            self.pos = vec((620, 360))
            print('you have died!')

    def normal(self):
        """
        docstring
        """
        self.mover = 'normal'

    def character_image(self):
        """
        docstring
        """
        if self.attacking > 0:
            self.attacking -= 1
            if self.direction == 'right':
                self.image = self.images['attack_r']
            else:
                self.image = self.images['attack_l']
            if self.attacking == 0 and self.direction == 'left':
                self.pos.x += 30
        else:
            self.hitbox = pygame.Rect(0,0,0,0)
            if self.direction == 'right':
                self.image = self.images['right']
            else:
                self.image = self.images['left']
