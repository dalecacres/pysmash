"""
Class for Mario
"""
import pygame
from spritesheet import SpriteSheet
from player import Player
from fireball import Fireball

vec = pygame.math.Vector2

def motion(self, name, mod, sprite_pos, start_vec, scale, spacer, height):
    if self.animation != name:
        self.animation = name
        self.tick[name] = 0
    self.tick[name] = (self.tick[name] + 1) % mod[0]

    tick = self.tick[name] // mod[1]
    x = start_vec.x
    frames = sprite_pos
    self.prev_frame = frames[tick] if frames[tick] else self.prev_frame
    for frame in frames[:tick]:
        x += frame + spacer

    return pygame.transform.scale(
        self.spritesheet.image_at((x, start_vec.y, self.prev_frame, height), (47, 54, 153)), scale
    )

def motion_flip(self, name, func):
    if self.animation != name:
        self.animation = name
    return pygame.transform.flip(func(), flip_x=True, flip_y=False)

class Mario(Player):
    """
    Class for Mario character
    """

    def __init__(self):
        """
        Creates Player object with Mario's attributes

        Room for expansion with custom functions/attacks
        """
        pygame.init()
        self.tick = {
            'stand': 0,
            'move': 0,
            'neutral_smash': 0,
            'neutral_tilt':0 ,
            'neutral_b': 0,
            'jump':0,
            'neutral_aerial': 0,
            'up_smash': 0,
        }

        self.prev_frame = 0
        self.animation = None

        self.projectiles = []
        self.spritesheet = SpriteSheet("resources/mario_sheet.png")

        right = pygame.transform.scale(
            self.spritesheet.image_at((17, 24, 25, 38), (47, 54, 153)), (50, 76)
        )
        left = pygame.transform.flip(right, flip_x=True, flip_y=False)
        tilt_r = pygame.transform.scale(
            self.spritesheet.image_at((46, 1003, 44, 31), (47, 54, 153)),
            (88, 62),
        )
        tilt_l = pygame.transform.flip(tilt_r, flip_x=True, flip_y=False)
        smash_r = pygame.transform.scale(
            self.spritesheet.image_at((73, 303, 47, 43), (47, 54, 153)),
            (96, 86),
        )
        smash_l = pygame.transform.flip(smash_r, flip_x=True, flip_y=False)

        self.size_ratios = {
            "standard": (50, 76)
        }

        self.animate = {
            "left": self.a_left,
            "right": self.a_right,
            "move_left": self.a_move_left,
            "move_right": self.a_move_right,
            "n_b_r": self.a_n_b_r,
            "n_b_l": self.a_n_b_l,
            "n_tilt_r": self.a_n_tilt_r,
            "n_tilt_l": self.a_n_tilt_l,
            "n_smash_r": self.a_n_smash_r,
            "n_smash_l": self.a_n_smash_l,
            "aerial_l": self.a_aerial_l,
            "aerial_r": self.a_aerial_r,
            "jump_right": self.a_jump_right,
            "jump_left": self.a_jump_left,
            "up_smash_r": self.a_u_smash_r,
            "up_smash_l": self.a_u_smash_l
        }

        self.images = {
            "left": left,
            "right": right,
            "tilt_r": tilt_r,
            "tilt_l": tilt_l,
            "smash_r": smash_r,
            "smash_l": smash_l,
        }
        super().__init__()

        self.name = "mario"
        self.weight = 5
        self.speed = 2.5
        self.smash_cooldown = 75
        self.hurtbox = pygame.Rect(self.rect.x, self.rect.y, 50, 76)
        self.attacks = {
            "neutral_tilt": {"damage": 10, "base": 5, "ratio": 2 / 3},
            "neutral_smash": {"damage": 30, "base": 10, "ratio": 2 / 3},
            "neutral_b": {"damage": 30, "base": 10, "ratio": 2 / 3},
            "up_smash": {"damage": 30, "base": 10, "ratio": 2 / 3},
        }


    def a_left(self):
        return motion_flip(self, "stand", self.a_right)

    def a_right(self):
        return motion(self, "stand", (72, 12), [25, 25, 25, 25, 25, 25], vec(17, 23), self.size_ratios['standard'], spacer=2, height=38)

    def a_move_left(self):
        return motion_flip(self, "move", self.a_move_right)

    def a_move_right(self):
        return motion(self, "move", (24, 3), [28, 30, 29, 24, 28, 30, 28, 24], vec(12, 149), self.size_ratios['standard'], spacer=6, height=38)

    def a_jump_left(self):
        return motion_flip(self, "jump", self.a_jump_right)

    def a_jump_right(self):
        return motion(self, "jump", (96, 16), [26, 0, 29, 0, 31, 26, 26, 26], vec(14, 83), self.size_ratios['standard'], spacer=4, height=44)

    def a_n_b_l(self):
        return motion_flip(self, "neutral_b", self.a_n_b_r)

    def a_n_b_r(self):
        return motion(self, "neutral_b", (50, 5), [35, 36, 36, 36, 31, 38, 31, 21, 27, 25], vec(10, 1445), self.size_ratios['standard'], spacer=6, height=36)

    def a_n_tilt_l(self):
        return motion_flip(self, "neutral_tilt", self.a_n_tilt_r)

    def a_n_tilt_r(self):
        return motion(self, "neutral_tilt", (50, 5), [36, 48, 44, 34, 34, 31, 31, 44, 40, 35], vec(6, 261), self.size_ratios['standard'], spacer=6, height=38)

    def a_n_smash_l(self):
        return motion_flip(self, "neutral_smash", self.a_n_smash_r)

    def a_n_smash_r(self):
        return motion(self, "neutral_smash", (35, 5), [28, 23, 49, 40, 32, 22, 26], vec(14, 303), self.size_ratios['standard'], spacer=4, height=44)

    def a_aerial_l(self):
        return motion_flip(self, "neutral_aerial", self.a_aerial_r)

    def a_aerial_r(self):
        return motion(self, "neutral_aerial", (40, 10), [31, 36, 31, 29], vec(11, 386), self.size_ratios['standard'], spacer=6, height=42)

    # def a_f_tilt_l(self):
    #     return motion_flip()
    # def a_f_tilt_r(self):
    #     return motion(self, "forward_tilt", )
    # def a_b_tilt_l(self):
    #     return motion_flip()
    # def a_b_tilt_r(self):
    #     return motion()
    # def a_u_tilt_l(self):
    #     return motion_flip()
    # def a_u_tilt_r(self):
    #     return motion()

    # def a_f_smash_l(self):
    #     return motion_flip()
    # def a_f_smash_r(self):
    #     return motion()
    # def a_b_smash_l(self):
    #     return motion_flip()
    # def a_b_smash_r(self):
    #     return motion()
    def a_u_smash_l(self):
        return motion_flip(self, "up_smash", self.a_u_smash_r)

    def a_u_smash_r(self):
        return motion(self, "up_smash", (70, 10), [39, 28, 22, 39, 36, 22, 25], vec(12, 456), (60, 100), spacer=6, height=57)
    # def a_f_b_l(self):
    #     return motion_flip()
    # def a_f_b_r(self):
    #     return motion()
    # def a_b_b_l(self):
    #     return motion_flip()
    # def a_b_b_r(self):
    #     return motion()
    # def a_u_b_l(self):
    #     return motion_flip()
    # def a_u_b_r(self):
    #     return motion()

    def set_boxes(self):
        """
        Update Mario's hitboxes and hurtboxes
        """
        if self.attack_cooldown > 0:
            if self.attack == "neutral_tilt":
                if self.direction == "left":
                    self.hurtbox = pygame.Rect(
                        self.rect.x + 38, self.rect.y, 50, 76
                    )
                    self.hitbox = pygame.Rect(
                        self.rect.x, self.rect.y + 15, 40, 35
                    )
                else:
                    self.hurtbox = pygame.Rect(self.rect.x, self.rect.y, 50, 76)
                    self.hitbox = pygame.Rect(
                        self.rect.x + 50, self.rect.y + 15, 40, 35
                    )
            if self.attack == "neutral_aerial":
                if self.direction == "left":
                    self.hurtbox = pygame.Rect(
                        self.rect.x + 50, self.rect.y + 10, 46, 76
                    )
                    self.hitbox = pygame.Rect(
                        self.rect.x, self.rect.y - 15, 59, 109
                    )
                else:
                    self.hurtbox = pygame.Rect(
                        self.rect.x, self.rect.y + 10, 46, 76
                    )
                    self.hitbox = pygame.Rect(
                        self.rect.x + 35, self.rect.y - 15, 59, 109
                    )
        else:
            self.hurtbox = pygame.Rect(self.rect.x, self.rect.y, 50, 76)
            self.hitbox = pygame.Rect(0, 0, 0, 0)
    
    def neutral_b(self):
        """
        Perform a tilt attack
        """
        if self.direction == "left":
            modifier = vec(-0.6, -40)
        else:
            modifier = vec(0.6, -40)
        self.projectiles.append(Fireball(self.direction, self.pos + modifier))
        self.attack = "neutral_b"
        self.attack_cooldown = 50
        if self.direction == "left":
            self.pos.x -= 30

    def neutral_tilt(self):
        """
        Perform a tilt attack
        """
        self.attack = "neutral_tilt"
        self.attack_cooldown = 25
        if self.direction == "left":
            self.pos.x -= 30

    def neutral_smash(self):
        """
        Perform a tilt attack
        """
        self.attack = "neutral_smash"
        self.attack_cooldown = 25
        if self.direction == "left":
            self.pos.x -= 30

    def aerial(self):
        """
        Perform a aerial attack
        """
        self.attack = "aerial"
        self.attack_cooldown = 25

    def up_smash(self):
        self.attack = "up_smash"
        self.attack_cooldown = 25
        if self.direction == "left":
            self.pos.x -= 30