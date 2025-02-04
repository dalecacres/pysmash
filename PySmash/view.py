"""
Viewers for PySmash
"""
from abc import ABC, abstractmethod
import pygame


class CharaterView(ABC):
    """
    Abstract Class for PySmash View
    """

    def __init__(self, game):
        """
        Construct a View object with the game as a parameter

        Args:
            game (Game): game to view
        """
        self._game = game

    @property
    def game(self):
        """
        Property that returns the game being viewed
        """
        return self._game

    @abstractmethod
    def draw(self):
        """
        A method that is an abstract method that does nothing
        """
        pass


class WindowView(CharaterView):
    """
    Class that draws the viewer to a PyGame window
    """

    def __init__(self, game, screen):
        """
        Construct a WindowView object and create the window itself

        Args:
            game (Game): Game object to draw to screen
            x_dim (int): x dimension of window
            y_dim (int): y dimension of window
        """
        super().__init__(game)
        self.screen = screen

    def draw(self):
        """
        Implement the 'draw' method, which draws the stage and sprites to
        the screen
        """
        self.game.all_sprites.update()
        self.screen.blit(self.game.stage.image, (0, 0))
        # self.game.stage.platforms.draw(self.screen)
        # pygame.draw.rect(self.screen, (255,255,255),
        #          self.game.player1.hurtbox, 1)
        # pygame.draw.rect(self.screen, (0,255,0), self.game.player1.hitbox, 1)
        # pygame.draw.rect(self.screen, (255,255,255),
        #         self.game.player2.hurtbox, 1)
        # pygame.draw.rect(self.screen, (255,0,0), self.game.player1.rect, 1)
        self.game.all_sprites.draw(self.screen)
        color = (255, 255, 255)
        small_font = pygame.font.SysFont("Corbel", 20)
        medium_font = pygame.font.SysFont("Corbel", 35)
        p1_line1 = small_font.render(f"Player 1 ", True, color)
        p1_line2 = small_font.render(f"{self._game.player1.name.capitalize()}:", True, color)
        p1_line3 = medium_font.render(f"{self._game.player1.health} %", True, color)
        p1_line4 = medium_font.render(f"•" * self._game.player1.stocks, True, color)
        p2_line1 = small_font.render(f"Player 2 ", True, color)
        p2_line2 = small_font.render(f"{self._game.player2.name.capitalize()}:", True, color)
        p2_line3 = medium_font.render(f"{self._game.player2.health} %", True, color)
        p2_line4 = medium_font.render(f"•" * self._game.player2.stocks, True, color)
        text_width, _ = small_font.size("Player 1")
        self.screen.blit(p1_line1, (395 - 155 - text_width * 2.2, 600))
        self.screen.blit(p1_line2, (395 - 155 - text_width * 2.2, 620))
        self.screen.blit(p1_line3, (395 - 155 - text_width * 2.2, 640))
        self.screen.blit(p1_line4, (395 - 155 - text_width * 2.2, 670))
        self.screen.blit(p2_line1, (1000, 600))
        self.screen.blit(p2_line2, (1000, 620))
        self.screen.blit(p2_line3, (1000, 640))
        self.screen.blit(p2_line4, (1000, 670))
        pygame.display.flip()
