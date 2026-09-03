import os
import pygame
from typing import Any

from settings import *
from bullet import Bullet


class Soldier(pygame.sprite.Sprite):
    def __init__(
        self,
        char_type: str,
        x: int,
        y: int,
        scale: int,
        speed: int,
        ammo: int,
        grenade: int = 0,
    ) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.alives: bool = True
        self.char_type: str = char_type
        self.health: int = 100
        self.max_health: int = self.health
        self.speed: int = speed
        self.ammo: int = ammo
        self.start_ammo: int = ammo
        self.grenade: int = grenade
        # self.start_grenade: int = grenade
        self.shoot_cooldown: int = 0
        self.direction: int = 1
        self.vel_y: float = 0
        self.jump: bool = False
        self.in_air: bool = True
        self.flip: bool = False

        # Advanced Type Hint: List of Lists containing Surfaces
        self.animation_list: list[list[pygame.surface.Surface]] = []

        self.frame_index: int = 0
        self.action: int = 0
        self.update_time: float = float(pygame.time.get_ticks())

        # load all images for the player
        animation_type: list[str] = ["Idle", "Run", "Jump", "Death"]
        for animation in animation_type:
            # reset temporary list of images
            temp_list: list[pygame.surface.Surface] = []
            # count number of files in the folder
            num_of_frames: int = len(os.listdir(f"img/{self.char_type}/{animation}"))
            for i in range(num_of_frames):
                img: pygame.surface.Surface = pygame.image.load(
                    f"img/{self.char_type}/{animation}/{i}.png"
                ).convert_alpha()
                img = pygame.transform.scale(
                    img, (int(img.get_width() * scale), int(img.get_height() * scale))
                ).convert_alpha()
                temp_list.append(img)

            self.animation_list.append(temp_list)

        self.image: pygame.surface.Surface = self.animation_list[self.action][
            self.frame_index
        ]
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self) -> None:
        self.update_animation()
        self.check_alive()
        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left: bool, moving_right: bool) -> None:
        # Reset movement var
        dx: float = 0
        dy: float = 0

        # assign movement var
        if moving_left:
            dx = float(-self.speed)
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = float(self.speed)
            self.flip = False
            self.direction = 1

        # jump
        if self.jump and not self.in_air:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # applying gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        # update rect position
        self.rect.x += int(dx)
        self.rect.y += int(dy)

    def shoot(
        self,
        bullet_group: pygame.sprite.Group,
        bullet_image: pygame.surface.Surface,
    ) -> None:
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet: Bullet = Bullet(
                self.rect.centerx + int(0.6 * self.rect.size[0] * self.direction),
                self.rect.centery,
                self.direction,
                bullet_image,
            )
            bullet_group.add(bullet)
            # reduse the ammo
            self.ammo -= 1

    def update_animation(self) -> None:
        ANIMATION_COOLDOWN: float = 100
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = float(pygame.time.get_ticks())
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alives = False
            self.update_action(3)

    def draw(self, window: pygame.surface.Surface) -> None:  # Added window type hint
        window.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        pygame.draw.rect(
            window,
            RED,
            (
                self.rect.x,
                self.rect.y - 20,
                self.rect.width,
                10,
            ),
        )

    def update_action(self, new_action: int) -> None:
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = float(pygame.time.get_ticks())
