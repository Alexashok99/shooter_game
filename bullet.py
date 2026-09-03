from typing import Any

import pygame

from settings import *


class Bullet(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        direction: int,
        image: pygame.surface.Surface,
        *groups: Any,
    ) -> None:
        super().__init__(*groups)
        self.speed: int = 10
        self.image: pygame.surface.Surface = image
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction: int = direction

    def update(
        self,
        player: Any,
        enemies: pygame.sprite.Group,
    ) -> None:
        # move bullets
        self.rect.x += self.direction * self.speed

        # check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > WIN_WIDTH:
            self.kill()

        # check collision with characters
        if player.alives and self.rect.colliderect(player.rect):
            player.health -= 5
            self.kill()
            return
        for enemy in enemies:
            if enemy.alives and self.rect.colliderect(enemy.rect):
                enemy.health -= 25
                self.kill()
                break
