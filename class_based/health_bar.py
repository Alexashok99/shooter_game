

import pygame
from class_based.settings import *

class HealthBar:
    def __init__(self, x: int, y: int, health: int, max_health: int) -> None:
        self.x: int = x
        self.y: int = y
        self.health: int = health
        self.max_health: int = max_health

    def draw(self, window: pygame.surface.Surface, health: int) -> None:
        self.health = health
        # calculate health ratio
        ratio: float = self.health / self.max_health
        pygame.draw.rect(window, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(window, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(window, GREEN, (self.x, self.y, 150 * ratio, 20))
