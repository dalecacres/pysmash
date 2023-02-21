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

    pygame.transform.scale(
        self.spritesheet.image_at((x, start_vec.y, self.prev_frame, height), (47, 54, 153)), scale
    )
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
            "move": 0,
            "stand": 0,
            "jump": 0,
            "neutral_b": 0,
            "neutral_tilt": 0,
            "neutral_smash": 0,
            "neutral_aerial": 0,
            "forward_aerial": 0,
            "up_aerial": 0,
            "down_aerial": 0,
            "forward_tilt": 0,
            "up_tilt": 0,
            "down_tilt": 0,
            "forward_smash": 0,
            "up_smash": 0,
            "down_smash": 0,
            "forward_b": 0,
            "up_b": 0,
            "down_b": 0,
        }

        self.prev_frame = 0
        self.animation = None

        self.projectiles = []
        self.spritesheet = SpriteSheet("resources/mario_sheet.png")

        # right = pygame.transform.scale(
        #     self.spritesheet.image_at((17, 24, 25, 38), (47, 54, 153)), (50, 76)
        # )
        # left = pygame.transform.flip(right, flip_x=True, flip_y=False)
        # tilt_r = pygame.transform.scale(
        #     self.spritesheet.image_at((46, 1003, 44, 31), (47, 54, 153)),
        #     (88, 62),
        # )
        # tilt_l = pygame.transform.flip(tilt_r, flip_x=True, flip_y=False)
        # smash_r = pygame.transform.scale(
        #     self.spritesheet.image_at((73, 303, 47, 43), (47, 54, 153)),
        #     (96, 86),
        # )
        # smash_l = pygame.transform.flip(smash_r, flip_x=True, flip_y=False)

        self.size_ratios = {
            "standard": (50, 76),
            "wide": (60, 76)
        }

        self.animate = {
            "stand_left": self.a_stand_l,
            "stand_right": self.a_stand_r,
            "move_left": self.a_move_l,
            "move_right": self.a_move_r,
            "jump_left": self.a_jump_l,
            "jump_right": self.a_jump_r,
            "neutral_b_left": self.a_n_b_l,
            "neutral_b_right": self.a_n_b_r,
            "neutral_tilt_left": self.a_n_tilt_l,
            "neutral_tilt_right": self.a_n_tilt_r,
            "neutral_smash_left": self.a_n_smash_l,
            "neutral_smash_right": self.a_n_smash_r,
            "neutral_aerial_left": self.a_n_aerial_l,
            "neutral_aerial_right": self.a_n_aerial_r,
            "forward_aerial_left": self.a_f_aerial_l,
            "forward_aerial_right": self.a_f_aerial_r,
            "up_aerial_left": self.a_u_aerial_l,
            "up_aerial_right": self.a_u_aerial_r,
            "down_aerial_left": self.a_d_aerial_l,
            "down_aerial_right": self.a_d_aerial_r,
            "forward_tilt_left": self.a_f_tilt_l,
            "forward_tilt_right": self.a_f_tilt_r,
            "up_tilt_left": self.a_u_tilt_l,
            "up_tilt_right": self.a_u_tilt_r,
            "down_tilt_left": self.a_d_tilt_l,
            "down_tilt_right": self.a_d_tilt_r,
            "forward_smash_left": self.a_f_smash_l,
            "forward_smash_right": self.a_f_smash_r,
            "up_smash_left": self.a_u_smash_l,
            "up_smash_right": self.a_u_smash_r,
            "down_smash_left": self.a_d_smash_l,
            "down_smash_right": self.a_d_smash_r,
            "forward_b_left": self.a_f_b_l,
            "forward_b_right": self.a_f_b_r,
            "up_b_left": self.a_u_b_l,
            "up_b_right": self.a_u_b_r,
            "down_b_left": self.a_d_b_l,
            "down_b_right": self.a_d_b_r,
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


    def a_stand_l(self):
        return motion_flip(self, "stand", self.a_stand_r)
    def a_stand_r(self):
        return motion(self, "stand", (60, 10), [25, 25, 25, 25, 25, 25], vec(18, 23), self.size_ratios['standard'], spacer=2, height=39)
    def a_move_l(self):
       return motion_flip(self, "move", self.a_move_r)
    def a_move_r(self):
        return motion(self, "move", (24, 3), [28, 30, 29, 24, 28, 30, 28, 24], vec(12, 149), self.size_ratios['standard'], spacer=6, height=38)
    def a_jump_l(self):
        return motion_flip(self, "jump", self.a_jump_r)
    def a_jump_r(self):
        return motion(self, "jump", (96, 16), [26, 0, 27, 0, 27, 26, 26, 26], vec(14, 83), self.size_ratios['standard'], spacer=4, height=44)
    def a_n_b_l(self):
        return motion_flip(self, "neutral_b", self.a_n_b_r)
    def a_n_b_r(self):
        return motion(self, "neutral_b", (50, 5), [35, 36, 36, 36, 31, 38, 31, 21, 27, 25], vec(10, 1445), self.size_ratios['standard'], spacer=6, height=36)
    def a_n_tilt_l(self):
        return motion_flip(self, "neutral_tilt", self.a_n_tilt_r)
    def a_n_tilt_r(self):
        return motion(self, "neutral_tilt", (50, 5), [36, 48, 44, 34, 34, 31, 31, 44, 40, 35], vec(6, 261), self.size_ratios['wide'], spacer=6, height=38)
    def a_n_smash_l(self):
        return motion_flip(self, "neutral_smash", self.a_n_smash_r)
    def a_n_smash_r(self):
        return motion(self, "neutral_smash", (35, 5), [28, 23, 49, 40, 32, 22, 26], vec(14, 303), self.size_ratios['standard'], spacer=4, height=44)


    def a_n_aerial_l(self):
        return motion_flip(self, "neutral_aerial", self.a_n_aerial_r)
    def a_n_aerial_r(self):
        return motion(self, "neutral_aerial", (40, 10), [31, 36, 31, 29], vec(11, 386), self.size_ratios['standard'], spacer=6, height=42)
    def a_f_aerial_l(self):
        return motion_flip(self, "forward_aerial", self.a_f_aerial_r)
    def a_f_aerial_r(self):
        return motion(self, "forward_aerial", (110, 10), [32, 32, 32, 35, 29, 44, 42, 32, 30, 34, 36], vec(14, 1068), self.size_ratios['standard'], spacer=6, height=40)
    def a_u_aerial_l(self):
        return motion_flip(self, "up_aerial", self.a_u_aerial_r)
    def a_u_aerial_r(self):
        return motion(self, "up_aerial", (80, 10), [37, 50, 37, 38, 38, 37, 23, 29], vec(14, 611), self.size_ratios['standard'], spacer=6, height=77)
    def a_d_aerial_l(self):
        return motion_flip(self, "down_aerial", self.a_d_aerial_r)
    def a_d_aerial_r(self):
        return motion(self, "down_aerial", (70, 10), [31, 24, 26, 29, 27, 28, 30], vec(12, 853), self.size_ratios['standard'], spacer=6, height=40)

    def a_f_tilt_l(self):
        return motion_flip(self, "forward_tilt", self.a_f_tilt_r)
    def a_f_tilt_r(self):
        return motion(self, "forward_tilt", (90, 10), [26, 45, 39, 36, 34, 32, 33, 33, 25], vec(13, 998),  self.size_ratios['wide'], spacer=6, height=36)
    def a_u_tilt_l(self):
        return motion_flip(self, "up_tilt", self.a_u_tilt_r)
    def a_u_tilt_r(self):
        return motion(self, "up_tilt", (70, 10), [35, 34, 22, 30, 20, 22, 22], vec(14, 557), self.size_ratios['standard'], spacer=5, height=53)
    def a_d_tilt_l(self):
        return motion_flip(self, "down_tilt", self.a_d_tilt_r)
    def a_d_tilt_r(self):
        return motion(self, "down_tilt", (60, 10), [25, 51, 34, 32, 28, 30], vec(14, 789), self.size_ratios['wide'], spacer=7, height=34)

    def a_f_smash_l(self):
        return motion_flip(self, "forward_smash", self.a_f_smash_r)
    def a_f_smash_r(self):
        return motion(self, "forward_smash", (70, 10), [24, 27, 26, 27, 42, 37, 25], vec(13, 922), self.size_ratios['wide'], spacer=6, height=44)
    def a_u_smash_l(self):
        return motion_flip(self, "up_smash", self.a_u_smash_r)
    def a_u_smash_r(self):
        return motion(self, "up_smash", (70, 10), [39, 28, 22, 39, 36, 22, 25], vec(14, 537), self.size_ratios['standard'], spacer=5, height=53)
    def a_d_smash_l(self):
        return motion_flip(self, "down_smash", self.a_d_smash_r)
    def a_d_smash_r(self):
         return motion(self, "down_smash", (90, 10), [29, 33, 38, 24, 41, 33, 22, 23, 25], vec(14, 727), self.size_ratios['standard'], spacer=8, height=40)


    def a_f_b_l(self):
        return motion_flip(self, "forward_b", self.a_f_b_r)
    def a_f_b_r(self):
        return motion(self, "forward_b", (110, 10), [22, 29, 23, 53, 47, 45, 26, 27, 38, 27, 25], vec(11, 1334), self.size_ratios['standard'], spacer=6, height=52)
    def a_u_b_l(self):
        return motion_flip(self, "up_b", self.a_u_b_r)
    def a_u_b_r(self):
        return motion(self, "up_b", (90, 10), [33, 38, 32, 27, 23, 24, 31, 33], vec(10, 1287), self.size_ratios['standard'], spacer=6, height=55)
    def a_d_b_l(self):
        return motion_flip(self, "down_b", self.a_d_b_r)
    def a_d_b_r(self):
        return motion(self, "down_b", (140, 10), [28, 26, 20, 36, 27, 22, 36, 30, 24, 36, 37, 37, 30, 25], vec(11, 1392), self.size_ratios['standard'], spacer=6, height=39)

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
        Perform a b attack
        """
        if self.direction == "left":
            modifier = vec(-0.6, -40)
        else:
            modifier = vec(0.6, -40)
        self.projectiles.append(Fireball(self.direction, self.pos + modifier))
        self.attack = "neutral_b"
        self.attack_cooldown = 50
        # if self.direction == "left":
            # self.pos.x -= 30

    def neutral_tilt(self):
        self.attack = "neutral_tilt"
        self.attack_cooldown = 50

    def neutral_smash(self):
        self.attack = "neutral_smash"
        self.attack_cooldown = 50

    def neutral_aerial(self):
        self.attack = "neutral_aerial"
        self.attack_cooldown = 50

    def forward_aerial(self):
        self.attack = "forward_aerial"
        self.attack_cooldown = 50

    def up_aerial(self):
        self.attack = "up_aerial"
        self.attack_cooldown = 50

    def down_aerial(self):
        self.attack = "down_aerial"
        self.attack_cooldown = 50

    def forward_tilt(self):
        self.attack = "forward_tilt"
        self.attack_cooldown = 50

    def up_tilt(self):
        self.attack = "up_tilt"
        self.attack_cooldown = 50

    def down_tilt(self):
        self.attack = "down_tilt"
        self.attack_cooldown = 50

    def forward_smash(self):
        self.attack = "forward_smash"
        self.attack_cooldown = 50

    def up_smash(self):
        self.attack = "up_smash"
        self.attack_cooldown = 50

    def down_smash(self):
        self.attack = "down_smash"
        self.attack_cooldown = 50

    def forward_b(self):
        self.attack = "forward_b"
        self.attack_cooldown = 50

    def up_b(self):
        self.attack = "up_b"
        self.attack_cooldown = 50

    def down_b(self):
        self.attack = "down_b"
        self.attack_cooldown = 50