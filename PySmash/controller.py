"""
Contains Controller Classes for PySmash
"""
from abc import ABC, abstractmethod
import pygame


class Controller(ABC):
    """
    Abstract class to define a character controller
    """

    def __init__(self, player):
        """
        Creates a private instance attribute of a Smash player

        Args: player is an instance of Player
        """
        self._player = player

    @property
    def player(self):
        """
        player property that returns the Player object the controller controls
        """
        return self._player

    @abstractmethod
    def move(self):
        """
        A method that is an abstract method that does nothing
        """
        pass


class KeyboardController(Controller):
    """
    Controller that allows keyboard control of character
    """

    def move(self):
        """
        Takes keyboard input and moves Player object accordingly
        """
        self.player.gravity()

        # Support for keeping a key held down
        if self.player.attack_cooldown == 0 or \
            self.player.attack == "neutral_tilt":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.left()
            if keys[pygame.K_RIGHT]:
                self.player.right()
            # if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.player.jump_pressed:
                # self.player.jump()
            # elif keys[pygame.K_UP] or keys[pygame.K_SPACE]:
                # self.player.begin_jump()
                # self.player.jump_pressed = True 
            if keys[pygame.K_COMMA]:
                self.player.neutral_b()
            # if not keys[pygame.K_UP] and not keys[pygame.K_SPACE]:
                # self.player.jump_pressed = False
            if keys[pygame.K_PERIOD] and keys[pygame.K_UP]:
                self.player.up_smash()
            elif keys[pygame.K_PERIOD]:
                self.player.neutral_smash()
            if keys[pygame.K_SLASH] and not self.player.isGrounded:
                self.player.aerial()
            if keys[pygame.K_SLASH] and self.player.isGrounded:
                self.player.neutral_tilt()
        # Keys that must be repressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            else:
                pygame.event.post(event)
        self.player.move()


class KeyboardController2(Controller):
    """
    Controller that allows keyboard control of character
    """

    def move(self):
        """
        Takes keyboard input and moves Player object accordingly
        """
        self.player.gravity()
        # Support for keeping a key held down
        if self.player.attack_cooldown == 0 or \
            self.player.attack == "neutral_tilt":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.player.left()
            if keys[pygame.K_d]:
                self.player.right()
            if keys[pygame.K_w] and self.player.jump_pressed:
                self.player.jump()
            elif keys[pygame.K_w]:
                self.player.begin_jump()
                self.player.jump_pressed = True 
            if not keys[pygame.K_w]:
                self.player.jump_pressed = False

        # Keys that must be repressed
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if self.player.attack_cooldown == 0:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    elif event.key == pygame.K_1:
                        self.player.neutral_tilt()
                    elif event.key == pygame.K_2:
                        self.player.neutral_smash()
        self.player.move()
