"""
Battlefield stage class
"""
import pygame
from map import Map, Platform


class Battlefield(Map):
    """
    Define Battlefield stage object
    """

    def __init__(self):
        """
        Create platforms and construct Battlefield map
        """
        self.platforms = pygame.sprite.Group(Platform(1, 725, 260, 335))
        super().__init__("resources/bf.png", self.platforms)
