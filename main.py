import sys
import pygame
import os
from typing import Any

# Constant
WIN_HEIGHT: int = 500
WIN_WIDTH: int = 800

pygame.init()

# pygame setup
screen: pygame.surface.Surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Shooter")
clock: pygame.time.Clock = pygame.time.Clock()
FPS: int = 60

GRAVITY: float = 0.75

# Tile Size
TILE_SIZE: int = 40

# Player Action Variable
moving_left: bool = False
moving_right: bool = False
shoot: bool = False
grenade: bool = False
grenade_thrown: bool = False

# load images
# bullet
bullet_img: pygame.surface.Surface = pygame.image.load(
    "img/icons/bullet.png"
).convert_alpha()
# grenade
grenade_img: pygame.surface.Surface = pygame.image.load(
    "img/icons/grenade.png"
).convert_alpha()

# Define color (Strict Tuple Hinting)
BG: tuple[int, int, int] = (144, 201, 120)
RED: tuple[int, int, int] = (255, 0, 0)


def draw_bg() -> None:  # Added return type hint
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (WIN_WIDTH, 300))


class Soldier(pygame.sprite.Sprite):
    def __init__(
        self, char_type: str, x: int, y: int, scale: int, speed: int, ammo: int, grenade: int = 0
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

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet: Bullet = Bullet(
                self.rect.centerx + int(0.6 * self.rect.size[0] * self.direction),
                self.rect.centery,
                self.direction,
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

    def update_action(self, new_action: int) -> None:
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = float(pygame.time.get_ticks())


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: int, *groups: Any) -> None:
        super().__init__(*groups)
        self.timer: int = 100
        self.vel_y: float = -11
        self.speed: int = 7
        self.image: pygame.surface.Surface = grenade_img
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction: int = direction

    def update(self) -> None:
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
            explosion_group.add(explosion)

            # damage to anyone that is nearby
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE*2 and abs(self.rect.centery - player.rect.centery) < TILE_SIZE*2:
                player.health -= 50
                # # move player by the direction of the grenade
                # if self.direction == 1:
                #     player.rect.x += 20
                # else:
                #     player.rect.x -= 20
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE*2 and abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE*2:
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
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
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

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: int, *groups: Any) -> None:
        super().__init__(*groups)
        self.speed: int = 10
        self.image: pygame.surface.Surface = bullet_img
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction: int = direction

    def update(self) -> None:
        # move bullets
        self.rect.x += self.direction * self.speed

        # check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > WIN_WIDTH:
            self.kill()

        # check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alives:
                player.health -= 5
                self.kill()
        if pygame.sprite.spritecollide(enemy, bullet_group, False):
            if enemy.alives:
                # # move enemy by the direction of the bullet
                # if self.direction == 1:
                #     enemy.rect.x += 20
                # else:
                #     enemy.rect.x -= 20
                enemy.health -= 25
                self.kill()


# create sprite groups
enemy_group: pygame.sprite.Group = pygame.sprite.Group()
bullet_group: pygame.sprite.Group = pygame.sprite.Group()
grenade_group: pygame.sprite.Group = pygame.sprite.Group()
explosion_group: pygame.sprite.Group = pygame.sprite.Group()


player: Soldier = Soldier("player", 200, 200, 3, 5, 30, 5)
enemy: Soldier = Soldier("enemy", 500, 250, 3, 5, 20, 0)
enemy_group.add(enemy)
enemy2: Soldier = Soldier("enemy", 700, 250, 3, 5, 20, 0)
enemy_group.add(enemy2)

running: bool = True
while running:
    clock.tick(FPS)

    draw_bg()

    player.update()
    player.draw(screen)
    for enemy in enemy_group:
        enemy.draw(screen)
        enemy.update()

    # update and draw groups
    bullet_group.update()
    grenade_group.update()
    explosion_group.update()
    bullet_group.draw(screen)
    grenade_group.draw(screen)
    explosion_group.draw(screen)

    # update player actions
    if player.alives:
        if shoot:
            player.shoot()

        # throw grenade
        elif grenade and grenade_thrown == False and player.grenade > 0:
            grenade = Grenade(
                player.rect.centerx + 0.5 * player.rect.size[0] * player.direction,
                player.rect.top,
                player.direction,
            )
            grenade_group.add(grenade)
            # reduce grenades
            player.grenade -= 1
            grenade_thrown = True
        if player.in_air:
            player.update_action(2)  # 2: Jump
        elif moving_left or moving_right:
            player.update_action(1)  # 1: Run
        else:
            player.update_action(0)  # 0: Idle
        player.move(moving_left, moving_right)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_q:
                grenade = True
            if event.key == pygame.K_w and player.alives:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False

    pygame.display.update()

pygame.quit()
sys.exit()
