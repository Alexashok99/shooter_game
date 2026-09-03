from typing import Any

import pygame

from settings import *


class ItemBox(pygame.sprite.Sprite):
    def __init__(
        self,
        item_type: str,
        x: int,
        y: int,
        image: pygame.surface.Surface,
        item_boxes: dict[str, pygame.surface.Surface],
        *groups: Any,
    ) -> None:
        super().__init__(*groups)
        self.item_type: str = item_type
        self.image: pygame.surface.Surface = item_boxes[self.item_type]
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y+ (TILE_SIZE - self.image.get_height()))

    def update(self, player: Any) -> None:
        # check if player has picked up the box
        if self.rect.colliderect(player.rect):
            # check what kind of box it was
            if self.item_type == "Health":
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == "Ammo":
                player.ammo += 15
            elif self.item_type == "Grenade":
                player.grenade += 3
            # delete item box
            self.kill()