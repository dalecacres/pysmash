import abc
import pygame


vec = pygame.math.Vector2


class Projectile(abc.ABC, pygame.sprite.Sprite):
    """
    Abstract Class representing projectile in PySmash
    """

    def __init__(self, direction, pos):
        """
        Create projectile with default values

        Args:
            direction (str): direction the projectile starts the game facing, either
                'left' or 'right'
        """
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        self.image = self.animate["fire_left"]()
        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(0, 0, 0, 0)
        self.proj_tick = 0

        self.pos = pos
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        if self.direction == "left":
            self.vel = vec(-4, 0)
        else:
            self.vel = vec(4, 0)

        self.knockback_counter = 0

    def move(self):
        """
        Take the current acceleration and velocity, calculate projectile's position,
        and update the projectile's rectangle
        """
        self.proj_tick += 1
        if self.proj_tick > 20:
            if self.knockback_counter <= 0:
                self.vel += self.acc
                self.pos += self.vel
            else:
                self.vel += self.acc
                self.pos += self.vel
                self.knockback_counter -= 1

        self.object_image()
        self.rect.midbottom = self.pos

        self.is_dead()

    def is_dead(self):
        """
        Check if character is dead and if so reset their health, decrease their
        stocks, and respawn them
        """
        if not -400 <= self.pos.x <= 1640 or not -400 <= self.pos.y <= 1120:
            self.vel = vec((0, 0))

    def object_image(self):
        if round(self.vel.x) != 0:
            if self.vel.x > 0:
                self.image = self.animate["fire_right"]()
            elif self.vel.x < 0: 
                self.image = self.animate["fire_left"]()

    def gravity(self):
        """
        Apply acceleration due to gravity to player object except if on a
        platform
        """
        self.acc = vec(0, 0.5)
        if 185 < self.pos.x < (185 + 861) and 405 < ((self.pos.y - 70)) < 430:
            self.vel.y = 1
        if self.knockback_counter <= 0 and 400 > (self.pos.y - 70):
            hits = pygame.sprite.spritecollide(self, self.platforms, False)
            if hits:
                self.pos.y = hits[0].rect.top + 1
                self.vel.y = -7