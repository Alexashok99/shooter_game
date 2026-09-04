from typing import Any

import pygame

from class_based.settings import *


class Grenade(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        direction: int,
        image: pygame.surface.Surface,
        *groups: Any,
    ) -> None:
        super().__init__(*groups)
        self.timer: int = 100
        self.vel_y: float = -11
        self.speed: int = 7
        self.image: pygame.surface.Surface = image
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction: int = direction

    def update(
        self,
        player: Any,
        enemies: pygame.sprite.Group,
        explosions: pygame.sprite.Group,
    ) -> None:
        # move grenade
        self.vel_y += GRAVITY
        dx: float = self.direction * self.speed
        dy: float = self.vel_y

        # check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            # bounce
            self.vel_y *= -0.5
            # reduce speed
            self.speed -= 1
            # prevent speed from going negative
            if self.speed < 0:
                self.speed = 0

        # check collision with walls
        if self.rect.left + dx < 0 or self.rect.right + dx > WIN_WIDTH:
            self.direction *= -1
            dx = self.direction * self.speed

        # update grenade position
        self.rect.x += int(dx)
        self.rect.y += int(dy)

        # countdown timer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion: Explosion = Explosion(self.rect.centerx, self.rect.centery, 1.5)
            explosions.add(explosion)

            # damage to anyone that is nearby
            if (
                abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2
                and abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2
            ):
                player.health -= 50
                # # move player by the direction of the grenade
                # if self.direction == 1:
                #     player.rect.x += 20
                # else:
                #     player.rect.x -= 20
            for enemy in enemies:
                if (
                    abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2
                    and abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2
                ):
                    enemy.health -= 50
                # # move enemy by the direction of the grenade
                #     if self.direction == 1:
                #         enemy.rect.x += 20
                #     else:
                #         enemy.rect.x -= 20


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, scale: float, *groups: Any) -> None:
        super().__init__(*groups)
        self.images = []
        for num in range(1, 6):
            img: pygame.surface.Surface = pygame.image.load(
                f"img/explosion/exp{num}.png"
            ).convert_alpha()
            img = pygame.transform.scale(
                img, (int(img.get_width() * scale), int(img.get_height() * scale))
            )
            self.images.append(img)
        self.frame_index: int = 0
        self.image: pygame.surface.Surface = self.images[self.frame_index]
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter: int = 0

    def update(self) -> None:
        EXPLOSION_SPEED: int = 4
        # update explosion animation
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED and self.frame_index < len(self.images) - 1:
            self.counter = 0
            self.frame_index += 1
            self.image = self.images[self.frame_index]

        # if the animation is complete, delete the explosion
        if self.frame_index >= len(self.images) - 1 and self.counter >= EXPLOSION_SPEED:
            self.kill()
