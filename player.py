"""
Contains Class representing a player in PySmash
"""
import abc
import pygame


vec = pygame.math.Vector2
FRIC = -0.25


class Player(abc.ABC, pygame.sprite.Sprite):
    """
    Abstract Class representing player in PySmash

    Attributes:
        direction (str): direction player is facing
        health (int): Current health of player
        image (pygame.Image): Current image of player
        rect (pygame.rect): Current rect of player
        stocks (int): Stocks remaining
        pos (pygame.math.Vector2): XY player position
        vel (pygame.math.Vector2): XY player velocity
        acc (pygame.math.Vector2): XY player acceleration
        jump_count (int): number of jumps remaining
        knockback_counter (int): frames remaining in knockback period
        attack (str): last attack that was performed
        attack_cooldown (int): frames remaining until player can attack
        damage_cooldown (int): frames remaining until player can take damage

    The following attributes are character specific and set in respective
    subclasses:
        spritesheet (Spritesheet): Spritesheet to take player images from
        images (dict): dictionary of all of the various player images
        name (str): name of character
        weight (int): weight of character (affects knockback taken)
        speed (int): speed of character
        smash_cooldown (int): cooldown period after performing a smash attack
        hitbox (pygame.Rect): box that can do damage
        hurtbox (pygame.Rect): box on the player that can take damage
        attacks (dict): Dictionary of a player's attacks and their respective
            statistics
    """

    def __init__(self):
        """
        Create player object with default values

        Args:
            direction (str): direction the player starts the game facing, either
                'left' or 'right'
        """
        pygame.sprite.Sprite.__init__(self)
        self.direction = None
        self._health = 0
        self.image = self.animate["stand_left"]()
        self.rect = self.image.get_rect()
        self._stocks = 3
        self.hitbox = pygame.Rect(0, 0, 0, 0)

        self.pos = vec((620, 360))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.jump_count = 2
        self.isGrounded = False
        self.knockback_counter = 0
        self.attack = "tilt"
        self.attack_cooldown = 0
        self.damage_cooldown = 0

    def knockback(self, strength_y, direction, ratio):
        """
        Knock a character back based on knockback amount from an attack

        Args:
            strength (int): amount of knockback to apply to the character
        """
        if direction == "right":
            strength_x = strength_y
        elif direction == "left":
            strength_x = -strength_y
        else:
            strength_x = strength_y
        self.vel = vec(strength_x, -strength_y * ratio)
        self.damage_cooldown = 10
        self.knockback_counter = self.health / 10


    @abc.abstractmethod
    def forward_aerial(self):
        """
        Abstract method for a character's smash attack. Defined on a per
        character basis
        """
        pass

    @abc.abstractmethod
    def up_aerial(self):
        """
        Abstract method for a character's smash attack. Defined on a per
        character basis
        """
        pass

    @abc.abstractmethod
    def up_smash(self):
        """
        Abstract method for a character's smash attack. Defined on a per
        character basis
        """
        pass

    @abc.abstractmethod
    def down_aerial(self):
        """
        Abstract method for a character's smash attack. Defined on a per
        character basis
        """
        pass

    @abc.abstractmethod
    def forward_tilt(self):
        """
        Abstract method for a character's smash attack. Defined on a per
        character basis
        """
        pass

    @abc.abstractmethod
    def forward_smash(self):
        """
        Abstract method for a character's smash attack. Defined on a per
        character basis
        """
        pass

    @abc.abstractmethod
    def down_smash(self):
        """
        Abstract method for a character's smash attack. Defined on a per
        character basis
        """
        pass

    @abc.abstractmethod
    def forward_b(self):
        """
        Abstract method for a character's smash attack. Defined on a per
        character basis
        """
        pass

    @abc.abstractmethod
    def up_b(self):
        """
        Abstract method for a character's smash attack. Defined on a per
        character basis
        """
        pass

    @abc.abstractmethod
    def down_b(self):
        """
        Abstract method for a character's smash attack. Defined on a per
        character basis
        """
        pass

    @abc.abstractmethod
    def up_smash(self):
        """
        Abstract method for a character's smash attack. Defined on a per
        character basis
        """
        pass

    @abc.abstractmethod
    def up_tilt(self):
        """
        Abstract method for a character's tilt attack. Defined on a per
        character basis
        """
        pass

    @abc.abstractmethod
    def neutral_b(self):
        """
        Abstract method for a character's b attack. Defined on a per
        character basis
        """
        pass

    @abc.abstractmethod
    def neutral_tilt(self):
        """
        Abstract method for a character's tilt attack. Defined on a per
        character basis
        """
        pass

    @abc.abstractmethod
    def neutral_smash(self):
        """
        Abstract method for a character's smash attack. Defined on a per
        character basis
        """
        pass

    @abc.abstractmethod
    def neutral_aerial(self):
        """
        Abstract method for a character's aerial attack. Defined on a per
        character basis
        """
        pass

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
                self.isGrounded = True
                self.pos.y = hits[0].rect.top + 1
                self.vel.y = 0
                self.jump_count = 2

    @property
    def health(self):
        """
        Get player's current health
        """
        return self._health

    @health.setter
    def health(self, value):
        """
        Set player's health

        Args:
            value (int): value to set player's health to
        """
        self._health = value

    @property
    def stocks(self):
        """
        Get player's current stocks remaining
        """
        return self._stocks

    @stocks.setter
    def stocks(self, value):
        """
        Set player's stocks

        Args:
            value (int): value to set player's stocks to
        """
        self._stocks = value

    def begin_jump(self):
        self.isGrounded = False
        self.jump_count -= 1
        self.vel.y -= 2

    def jump(self):
        """
        Make the character jump
        """
        if self.isGrounded:
            self.begin_jump()
        elif not self.jump_count:
            return None
        elif self.vel.y > -10:
            self.vel.y -= 2
        else:
            self.begin_jump()


    def move_left(self):
        """
        Move the character left
        """
        self.acc.x = -self.speed
        # self.image = self.animate["move_left"]()
        self.image = self.animate["move_left"]()
        self.direction = "left"

    def move_right(self):
        """,
        Move, the character right
        """,
        self.acc.x = self.speed
        # self.image = self.animate["move_right"]()
        self.image = self.animate["move_right"]()
        self.direction = "right"

    def move(self):
        """
        Take the current acceleration and velocity, calculate player's position,
        and update the player's rectangle
        """
        if self.knockback_counter <= 0:
            self.acc.x += self.vel.x * FRIC
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc
        else:
            self.vel.y += self.acc.y
            self.pos += self.vel + 0.5 * self.acc
            self.knockback_counter -= 1

        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            # if self.attack_cooldown == 0 and self.direction == "left":
                # self.pos.x += 30
            
        self.character_image()
        self.set_boxes()
        self.rect.midbottom = self.pos

        self.is_dead()

    def is_dead(self):
        """
        Check if character is dead and if so reset their health, decrease their
        stocks, and respawn them
        """
        if not -400 <= self.pos.x <= 1640 or not -400 <= self.pos.y <= 1120:
            self._health = 0
            self._stocks -= 1
            self.pos = vec((620, 360))
            self.vel = vec((0, 0))
            self.attack_cooldown = 0

    def character_image(self):
        """
        Set
         which character image to be displayed
        """
        if self.attack_cooldown > 0:
            if self.attack == "jump":
                if self.direction == "left":
                    self.image = self.animate["jump_left"]()
                else:
                    self.image = self.animate["jump_right"]()
            if self.attack == "neutral_b":
                if self.direction == "left":
                    self.image = self.animate["neutral_b_left"]()
                else:
                    self.image = self.animate["neutral_b_right"]()
            if self.attack == "neutral_tilt":
                if self.direction == "left":
                    self.image = self.animate["neutral_tilt_left"]()
                else:
                    self.image = self.animate["neutral_tilt_right"]()
            if self.attack == "neutral_smash":
                if self.direction == "left":
                    self.image = self.animate["neutral_smash_left"]()
                else:
                    self.image = self.animate["neutral_smash_right"]()
            if self.attack == "neutral_aerial":
                if self.direction == "left":
                    self.image = self.animate["neutral_aerial_left"]()
                else:
                    self.image = self.animate["neutral_aerial_right"]()
            if self.attack == "forward_aerial":
                if self.direction == "left":
                    self.image = self.animate["forward_aerial_left"]()
                else:
                    self.image = self.animate["forward_aerial_right"]()
            if self.attack == "up_aerial":
                if self.direction == "left":
                    self.image = self.animate["up_aerial_left"]()
                else:
                    self.image = self.animate["up_aerial_right"]()
            if self.attack == "down_aerial":
                if self.direction == "left":
                    self.image = self.animate["down_aerial_left"]()
                else:
                    self.image = self.animate["down_aerial_right"]()
            if self.attack == "forward_tilt":
                if self.direction == "left":
                    self.image = self.animate["forward_tilt_left"]()
                else:
                    self.image = self.animate["forward_tilt_right"]()
            if self.attack == "up_tilt":
                if self.direction == "left":
                    self.image = self.animate["up_tilt_left"]()
                else:
                    self.image = self.animate["up_tilt_right"]()
            if self.attack == "down_tilt":
                if self.direction == "left":
                    self.image = self.animate["down_tilt_left"]()
                else:
                    self.image = self.animate["down_tilt_right"]()
            if self.attack == "forward_smash":
                if self.direction == "left":
                    self.image = self.animate["forward_smash_left"]()
                else:
                    self.image = self.animate["forward_smash_right"]()
            if self.attack == "up_smash":
                if self.direction == "left":
                    self.image = self.animate["up_smash_left"]()
                else:
                    self.image = self.animate["up_smash_right"]()
            if self.attack == "down_smash":
                if self.direction == "left":
                    self.image = self.animate["down_smash_left"]()
                else:
                    self.image = self.animate["down_smash_right"]()
            if self.attack == "forward_b":
                if self.direction == "left":
                    self.image = self.animate["forward_b_left"]()
                else:
                    self.image = self.animate["forward_b_right"]()
            if self.attack == "up_b":
                if self.direction == "left":
                    self.image = self.animate["up_b_left"]()
                else:
                    self.image = self.animate["up_b_right"]()
            if self.attack == "down_b":
                if self.direction == "left":
                    self.image = self.animate["down_b_left"]()
                else:
                    self.image = self.animate["down_b_right"]()
                # if self.attack_cooldown == 0 and self.direction == "left":
                    # self.pos.x += 30
        elif round(self.vel.y) != 0:
            if self.direction == "right":
                self.image = self.animate["jump_right"]()
            else:
                self.image = self.animate["jump_left"]()
        elif round(self.vel.x) != 0:
            if self.vel.x > 0:
                self.image = self.animate["move_right"]()
            elif self.vel.x < 0: 
                self.image = self.animate["move_left"]()
        else:
            if self.direction == "right":
                self.image = self.animate["stand_right"]()
            else:
                self.image = self.animate["stand_left"]()