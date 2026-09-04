

from typing import Any

import pygame
from settings import *

class Decorator(pygame.sprite.Sprite):
    def __init__(
        self,
        image: pygame.surface.Surface,
        x: int,
        y: int,
        *groups: Any,
    ) -> None:
        super().__init__(*groups)
        self.image: pygame.surface.Surface = image
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

class Water(pygame.sprite.Sprite):
    def __init__(
        self,
        image: pygame.surface.Surface,
        x: int,
        y: int,
        *groups: Any,
    ) -> None:
        super().__init__(*groups)
        self.image: pygame.surface.Surface = image
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

class Exit(pygame.sprite.Sprite):
    def __init__(
        self,
        image: pygame.surface.Surface,
        x: int,
        y: int,
        *groups: Any,
    ) -> None:
        super().__init__(*groups)
        self.image: pygame.surface.Surface = image
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

