import sys
import pygame
from pygame import mixer
import os
import random
import csv
from typing import Any

import button

# Constant
WIN_WIDTH: int = 800
WIN_HEIGHT: int = int(0.8 * WIN_WIDTH)
# Frames Per Second
FPS: int = 60
# Gravity Constant
GRAVITY: float = 0.75
SCROLL_THRESH: int = 200
# Define number of rows and columns
ROWS: int = 16
COLS: int = 150
# Tile Size
TILE_SIZE: int = WIN_HEIGHT // ROWS
# Tile types
TILE_TYPES: int = 21

MAX_LEVELS: int = 3

screen_scroll: int = 0
bg_scroll: int = 0
level: int = 1
start_game: bool = False
start_intro: bool = False

# Define color (Strict Tuple Hinting)
BG: tuple[int, int, int] = (144, 201, 120)
RED: tuple[int, int, int] = (255, 0, 0)
GREEN: tuple[int, int, int] = (0, 255, 0)
WHITE: tuple[int, int, int] = (255, 255, 255)
BLACK: tuple[int, int, int] = (0, 0, 0)
PINK: tuple[int, int, int] = (235, 65, 54)
# Initialize Pygame
pygame.init()
# pygame setup
screen: pygame.surface.Surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Shooter")
clock: pygame.time.Clock = pygame.time.Clock()
# Player Action Variable
moving_left: bool = False
moving_right: bool = False
shoot: bool = False
grenade: bool = False
grenade_thrown: bool = False

# Load Music and sound
pygame.mixer.music.load("audio/music2.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)
jump_fx = pygame.mixer.Sound("audio/jump.wav")
jump_fx.set_volume(0.5)
shoot_fx = pygame.mixer.Sound("audio/shot.wav")
shoot_fx.set_volume(0.5)
grenade_fx = pygame.mixer.Sound("audio/grenade.wav")
grenade_fx.set_volume(0.5)

# load images
# Button images
start_img: pygame.surface.Surface = pygame.image.load(
    "img/start_btn.png"
).convert_alpha()
restart_img: pygame.surface.Surface = pygame.image.load(
    "img/restart_btn.png"
).convert_alpha()
exit_img: pygame.surface.Surface = pygame.image.load("img/exit_btn.png").convert_alpha()

# Load Background Images
pine1_img: pygame.surface.Surface = pygame.image.load(
    "img/background/pine1.png"
).convert_alpha()
pine2_img: pygame.surface.Surface = pygame.image.load(
    "img/background/pine2.png"
).convert_alpha()
mountain_img: pygame.surface.Surface = pygame.image.load(
    "img/background/mountain.png"
).convert_alpha()
sky_img: pygame.surface.Surface = pygame.image.load(
    "img/background/sky_cloud.png"
).convert_alpha()
# store tiles in a list
img_list: list[pygame.Surface] = []
for tile_id in range(TILE_TYPES):
    img: pygame.Surface = pygame.image.load(f"img/tile/{tile_id}.png")
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
# bullet
bullet_img: pygame.surface.Surface = pygame.image.load(
    "img/icons/bullet.png"
).convert_alpha()
# grenade
grenade_img: pygame.surface.Surface = pygame.image.load(
    "img/icons/grenade.png"
).convert_alpha()
health_box_img: pygame.surface.Surface = pygame.image.load(
    "img/icons/health_box.png"
).convert_alpha()
ammo_box_img: pygame.surface.Surface = pygame.image.load(
    "img/icons/ammo_box.png"
).convert_alpha()
grenade_box_img: pygame.surface.Surface = pygame.image.load(
    "img/icons/grenade_box.png"
).convert_alpha()
item_boxes: dict[str, pygame.surface.Surface] = {
    "Health": health_box_img,
    "Ammo": ammo_box_img,
    "Grenade": grenade_box_img,
}


def draw_text(
    text: str,
    font: pygame.font.Font,
    text_col: tuple[int, int, int],
    x: int,
    y: int,
) -> None:
    img: pygame.surface.Surface = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_bg() -> None:  # Added return type hint
    screen.fill(BG)
    for x in range(5):
        width = sky_img.get_width()
        screen.blit(sky_img, (x * width - bg_scroll * 0.5, 0))
        screen.blit(
            mountain_img,
            (
                x * width - bg_scroll * 0.6,
                WIN_HEIGHT - mountain_img.get_height() - 300,
            ),
        )
        screen.blit(
            pine1_img,
            (x * width - bg_scroll * 0.7, WIN_HEIGHT - pine1_img.get_height() - 150),
        )
        screen.blit(
            pine2_img,
            (x * width - bg_scroll * 0.8, WIN_HEIGHT - pine2_img.get_height()),
        )


# function to reset level
def reset_level():
    exit_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decorator_group.empty()
    water_group.empty()
    exit_group.empty()
    enemy_group.empty()

    # create empty tile list
    data: list[list[int]] = []
    for row in range(ROWS):
        r: list[int] = [-1] * COLS
        data.append(r)

    return data

class Character(pygame.sprite.Sprite):
    def __init__(
        self,
        char_folder: str,
        x: int,
        y: int,
        scale: float,
        speed: int,
        ammo: int,
        grenade: int = 0,
    ) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.alives: bool = True
        self.health: int = 100
        self.max_health: int = self.health
        self.speed: int = speed
        self.ammo: int = ammo
        self.start_ammo: int = ammo
        self.grenade: int = grenade
        self.shoot_cooldown: int = 0
        self.direction: int = 1
        self.vel_y: float = 0
        self.jump: bool = False
        self.in_air: bool = True
        self.flip: bool = False

        self.animation_list: list[list[pygame.surface.Surface]] = []

        self.frame_index: int = 0
        self.action: int = 0
        self.update_time: float = float(pygame.time.get_ticks())
        
        # Load all images for the character
        animation_type: list[str] = ["Idle", "Run", "Jump", "Death"]
        for animation in animation_type:
            temp_list: list[pygame.surface.Surface] = []
            num_of_frames: int = len(os.listdir(f"img/{char_folder}/{animation}"))
            for i in range(num_of_frames):
                img: pygame.surface.Surface = pygame.image.load(
                    f"img/{char_folder}/{animation}/{i}.png"
                ).convert_alpha()
                img = pygame.transform.scale(
                    img, (int(img.get_width() * scale), int(img.get_height() * scale))
                ).convert_alpha()
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image: pygame.surface.Surface = self.animation_list[self.action][self.frame_index]
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self) -> None:
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet: Bullet = Bullet(
                self.rect.centerx + int(0.75 * self.rect.size[0] * self.direction),
                self.rect.centery,
                self.direction,
            )
            bullet_group.add(bullet)
            self.ammo -= 1
            shoot_fx.play()

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

    def draw(self, window: pygame.surface.Surface) -> None:
        window.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        pygame.draw.rect(window, RED, (self.rect.x, self.rect.y - 20, 50, 10))

    def update_action(self, new_action: int) -> None:
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = float(pygame.time.get_ticks())


class Player(Character):
    def __init__(
        self, x: int, y: int, scale: float, speed: int, ammo: int, grenade: int
    ) -> None:
        super().__init__("player", x, y, scale, speed, ammo, grenade)

    def move(self, moving_left: bool, moving_right: bool) -> tuple[int, bool]:
        screen_scroll: int = 0
        dx: float = 0
        dy: float = 0

        if moving_left:
            dx = float(-self.speed)
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = float(self.speed)
            self.flip = False
            self.direction = 1

        if self.jump and not self.in_air:
            self.vel_y = -13
            self.jump = False
            self.in_air = True

        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0
            
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False

        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0

        level_complete: bool = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True

        if self.rect.bottom > WIN_HEIGHT:
            self.health = 0

        # Player specific screen edge check
        if self.rect.left + dx < 0 or self.rect.right + dx > WIN_WIDTH:
            dx = 0

        self.rect.x += int(dx)
        self.rect.y += int(dy)

        # Player specific screen scrolling
        if (self.rect.right > WIN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - WIN_WIDTH) or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
            self.rect.x -= int(dx)
            screen_scroll = -dx
            
        return screen_scroll, level_complete


class Enemy(Character):
    def __init__(
        self, x: int, y: int, scale: float, speed: int, ammo: int, grenade: int = 0
    ) -> None:
        super().__init__("enemy", x, y, scale, speed, ammo, grenade)
        self.move_counter: int = 0
        self.vision: pygame.Rect = pygame.Rect(0, 0, 150, 20)
        self.idling: bool = False
        self.idling_counter: int = 0

    def move(self, moving_left: bool, moving_right: bool) -> None:
        dx: float = 0
        dy: float = 0

        if moving_left:
            dx = float(-self.speed)
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = float(self.speed)
            self.flip = False
            self.direction = 1

        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0
                # Enemy specific wall hit logic
                self.direction *= -1
                self.move_counter = 0
            
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False

        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0

        if self.rect.bottom > WIN_HEIGHT:
            self.health = 0

        self.rect.x += int(dx)
        self.rect.y += int(dy)

    def ai(self) -> None:
        if self.alives and player.alives:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)  
                self.idling = True
                self.idling_counter = 50
                
            if self.vision.colliderect(player.rect):
                self.update_action(0)  
                self.shoot()
            else:
                if self.idling is False:
                    if self.direction == 1:
                        ai_moving_right: bool = True
                    else:
                        ai_moving_right: bool = False
                    ai_moving_left: bool = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)  
                    self.move_counter += 1
                    
                    self.vision.center = (
                        self.rect.centerx + 75 * self.direction,
                        self.rect.centery,
                    )
                    
                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

        # Enemy specific scroll logic
        self.rect.x += screen_scroll


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: int, *groups: Any) -> None:
        super().__init__(*groups)
        self.timer: int = 100
        self.vel_y: float = -11
        self.speed: int = 7
        self.image: pygame.surface.Surface = grenade_img
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width: int = self.image.get_width()
        self.height: int = self.image.get_height()
        self.direction: int = direction

    def update(self) -> None:
        # move grenade
        self.vel_y += GRAVITY
        dx: float = self.direction * self.speed
        dy: float = self.vel_y

        # check collision with level
        for tile in world.obstacle_list:
            # check collision in x direction
            if tile[1].colliderect(
                self.rect.x + dx, self.rect.y, self.width, self.height
            ):
                self.direction *= -1
                dx = self.direction * self.speed
            # check collision in y direction
            if tile[1].colliderect(
                self.rect.x, self.rect.y + dy, self.width, self.height
            ):
                self.speed = 0
                # check if below the ground i.e. throwing up
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                # check if above the ground i.e. falling
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0

        # update grenade position
        self.rect.x += int(dx) + screen_scroll
        self.rect.y += int(dy)

        # countdown timer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            grenade_fx.play()
            explosion: Explosion = Explosion(self.rect.centerx, self.rect.centery, 1.5)
            explosion_group.add(explosion)

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
            for enemy in enemy_group:
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
        # scroll
        self.rect.x += screen_scroll
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
        self.rect.x += self.direction * self.speed + screen_scroll

        # check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > WIN_WIDTH:
            self.kill()

        # check collision with walls
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
                break

        # check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alives:
                player.health -= 5
                self.kill()
        for enemy in enemy_group:
            if enemy.alives and self.rect.colliderect(enemy.rect):
                enemy.health -= 25
                self.kill()
                break


class World:
    def __init__(self) -> None:
        self.obstacle_list: list[tuple[pygame.Surface, pygame.Rect]] = []

    def process_data(self, data: list[list[int]]) -> tuple[Player, HealthBar]:
        self.level_length = len(data[0])
        # iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img: pygame.Surface = img_list[tile]
                    img_rect: pygame.Rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data: tuple[pygame.Surface, pygame.Rect] = (img, img_rect)

                    if 0 <= tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif 9 <= tile <= 10:  # water
                        water: Water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif 11 <= tile <= 14:  # decoration
                        decorator: Decorator = Decorator(
                            img, x * TILE_SIZE, y * TILE_SIZE
                        )
                        decorator_group.add(decorator)

                    # Inside process_data() method:
                    elif tile == 15:
                        # Instantiate the new Player class
                        player = Player(x * TILE_SIZE, y * TILE_SIZE, 1.65, 5, 20, 5)
                        health_bar = HealthBar(10, 10, player.health, player.max_health)
                    elif tile == 16:
                        # Instantiate the new Enemy class
                        enemy = Enemy(x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 20, 0)
                        enemy_group.add(enemy)
                    elif tile == 17:  # Create Ammo Box
                        item_box: ItemBox = ItemBox(
                            "Ammo", x * TILE_SIZE, y * TILE_SIZE
                        )
                        item_box_group.add(item_box)
                    elif tile == 18:  # Create Grenade Box
                        item_box = ItemBox("Grenade", x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 19:  # Create Health Box
                        item_box = ItemBox("Health", x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 20:  # create exits
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)

        if player is None or health_bar is None:
            raise ValueError("Player start position not found in level data.")

        return player, health_bar

    def draw(self) -> None:
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll  # Adjust the x-coordinate of the tile's rect
            screen.blit(tile[0], tile[1])


class Decorator(pygame.sprite.Sprite):
    def __init__(
        self,
        image: pygame.surface.Surface,
        x: int,
        y: int,
    ) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image: pygame.surface.Surface = image
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.midtop = (
            x + TILE_SIZE // 2,
            y + (TILE_SIZE - self.image.get_height()),
        )

    def update(self) -> None:
        self.rect.x += screen_scroll


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
        self.rect.midtop = (
            x + TILE_SIZE // 2,
            y + (TILE_SIZE - self.image.get_height()),
        )

    def update(self) -> None:
        self.rect.x += screen_scroll


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
        self.rect.midtop = (
            x + TILE_SIZE // 2,
            y + (TILE_SIZE - self.image.get_height()),
        )

    def update(self) -> None:
        self.rect.x += screen_scroll


class ItemBox(pygame.sprite.Sprite):
    def __init__(
        self,
        item_type: str,
        x: int,
        y: int,
        *groups: Any,
    ) -> None:
        super().__init__(*groups)
        self.item_type: str = item_type
        self.image: pygame.surface.Surface = item_boxes[self.item_type]
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.midtop = (
            x + TILE_SIZE // 2,
            y + (TILE_SIZE - self.image.get_height()),
        )

    def update(self) -> None:
        # scroll
        self.rect.x += screen_scroll
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


class ScreenFade:
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter: int = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:  # whole screen fade down
            pygame.draw.rect(
                screen,
                self.color,
                (0 - self.fade_counter, 0, WIN_WIDTH // 2, WIN_HEIGHT),
            )
            pygame.draw.rect(
                screen,
                self.color,
                (WIN_WIDTH // 2 + self.fade_counter, 0, WIN_WIDTH, WIN_HEIGHT),
            )
            pygame.draw.rect(
                screen,
                self.color,
                (0, 0 - self.fade_counter, WIN_WIDTH, WIN_HEIGHT // 2),
            )
            pygame.draw.rect(
                screen,
                self.color,
                (0, WIN_HEIGHT // 2 + self.fade_counter, WIN_WIDTH, WIN_HEIGHT),
            )
        if self.direction == 2:  # Vertical screen fade down
            pygame.draw.rect(
                screen, self.color, (0, 0, WIN_WIDTH, 0 + self.fade_counter)
            )
        if self.fade_counter >= WIN_WIDTH:
            fade_complete = True

        return fade_complete


death_fade = ScreenFade(2, PINK, 4)
intro_fade = ScreenFade(1, BLACK, 4)

# Create Button
start_button = button.Button(WIN_WIDTH // 2 - 130, WIN_HEIGHT // 2 - 150, start_img, 1)
exit_button = button.Button(WIN_WIDTH // 2 - 110, WIN_HEIGHT // 2 + 50, exit_img, 1)
restart_button = button.Button(
    WIN_WIDTH // 2 - 100, WIN_HEIGHT // 2 - 50, restart_img, 2
)

# create sprite groups
enemy_group: pygame.sprite.Group = pygame.sprite.Group()
bullet_group: pygame.sprite.Group = pygame.sprite.Group()
grenade_group: pygame.sprite.Group = pygame.sprite.Group()
explosion_group: pygame.sprite.Group = pygame.sprite.Group()
item_box_group: pygame.sprite.Group = pygame.sprite.Group()
water_group: pygame.sprite.Group = pygame.sprite.Group()
decorator_group: pygame.sprite.Group = pygame.sprite.Group()
exit_group: pygame.sprite.Group = pygame.sprite.Group()


# create empty tile list
world_data: list[list[int]] = []
for row in range(ROWS):
    r: list[int] = [-1] * COLS
    world_data.append(r)
# load in level data and create world
with open(f"level{level}_data.csv", newline="") as csvfile:
    reader: Any = csv.reader(csvfile, delimiter=",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            if 0 <= x < ROWS and 0 <= y < COLS:
                world_data[x][y] = int(tile)

world = World()
player, health_bar = world.process_data(world_data)


running: bool = True
while running:
    clock.tick(FPS)
    if start_game == False:
        # Draw Menu
        screen.fill(BG)
        # add button
        if start_button.draw(screen):
            start_game = True
            start_intro = True
        if exit_button.draw(screen):
            running = False
    else:
        # draw background
        draw_bg()
        # draw world map
        world.draw()
        # Show player stats
        health_bar.draw(screen, player.health)
        draw_text(
            f"Health: {player.health}", pygame.font.SysFont("consolas", 20), RED, 10, 10
        )
        draw_text(
            f"Ammo: {player.ammo}", pygame.font.SysFont("consolas", 20), RED, 10, 40
        )
        draw_text(
            f"Grenade: {player.grenade}",
            pygame.font.SysFont("consolas", 20),
            RED,
            10,
            70,
        )
        for x in range(player.grenade):
            screen.blit(grenade_img, (130 + (x * 15), 70))

        player.update()
        player.draw(screen)
        for enemy in enemy_group:
            enemy.ai()
            enemy.draw(screen)
            enemy.update()

        # update and draw groups
        bullet_group.update()
        grenade_group.update()
        explosion_group.update()
        item_box_group.update()
        water_group.update()
        decorator_group.update()
        exit_group.update()
        bullet_group.draw(screen)
        grenade_group.draw(screen)
        explosion_group.draw(screen)
        item_box_group.draw(screen)
        water_group.draw(screen)
        decorator_group.draw(screen)
        exit_group.draw(screen)

        # Show intro
        if start_intro == True:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0

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
            screen_scroll, level_complete = player.move(moving_left, moving_right)
            bg_scroll -= screen_scroll
            # check if player has complete leve
            if level_complete:
                start_intro = True
                level += 1
                bg_scroll = 0
                world_data = reset_level()
                if level <= MAX_LEVELS:
                    # Load in level data and create world
                    with open(f"level{level}_data.csv", newline="") as csvfile:
                        reader: Any = csv.reader(csvfile, delimiter=",")
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                if 0 <= x < ROWS and 0 <= y < COLS:
                                    world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(world_data)

        else:
            screen_scroll = 0
            if death_fade.fade():
                if restart_button.draw(screen):
                    death_fade.fade_counter = 0
                    start_intro = True
                    bg_scroll = 0
                    world_data = reset_level()
                    # load in level data and create world
                    with open(f"level{level}_data.csv", newline="") as csvfile:
                        reader: Any = csv.reader(csvfile, delimiter=",")
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                if 0 <= x < ROWS and 0 <= y < COLS:
                                    world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(world_data)

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
                jump_fx.play()
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
