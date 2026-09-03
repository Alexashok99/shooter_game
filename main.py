import sys
import pygame
import os
from typing import Any


from settings import *
from soldiers import Soldier
from bullet import Bullet
from grenade import Grenade, Explosion
from item_box import ItemBox

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

# load images
# bullet
bullet_img: pygame.surface.Surface = pygame.image.load(
    "img/icons/bullet.png"
).convert_alpha()
# grenade
grenade_img: pygame.surface.Surface = pygame.image.load(
    "img/icons/grenade.png"
).convert_alpha()
# pickup boxes
health_box_img: pygame.surface.Surface = pygame.image.load(
    "img/icons/health_box.png"
).convert_alpha()
ammo_box_img: pygame.surface.Surface = pygame.image.load(
    "img/icons/ammo_box.png"
).convert_alpha()
grenade_box_img: pygame.surface.Surface = pygame.image.load(
    "img/icons/grenade_box.png"
).convert_alpha()

# item boxes
item_boxes: dict[str, pygame.surface.Surface] = {
    "Health": health_box_img,
    "Ammo": ammo_box_img,
    "Grenade": grenade_box_img,
}

# Define font
font: pygame.font.Font = pygame.font.SysFont("Futura", 30)

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

def draw_text(
    text: str, font: pygame.font.Font, text_col: tuple[int, int, int], x: int, y: int
) -> None:
    img: pygame.surface.Surface = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_bg() -> None:  # Added return type hint
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (WIN_WIDTH, 300))


# create sprite groups
enemy_group: pygame.sprite.Group = pygame.sprite.Group()
bullet_group: pygame.sprite.Group = pygame.sprite.Group()
grenade_group: pygame.sprite.Group = pygame.sprite.Group()
explosion_group: pygame.sprite.Group = pygame.sprite.Group()
item_boxes_group: pygame.sprite.Group = pygame.sprite.Group()


# temp create some item boxes
item_box: ItemBox = ItemBox("Health", 100, 260, health_box_img, item_boxes)
item_boxes_group.add(item_box)
item_box2: ItemBox = ItemBox("Ammo", 400, 260, ammo_box_img, item_boxes)
item_boxes_group.add(item_box2)
item_box3: ItemBox = ItemBox("Grenade", 600, 260, grenade_box_img, item_boxes)
item_boxes_group.add(item_box3)

player: Soldier = Soldier("player", 200, 200, 3, 5, 30, 5)
health_bar: HealthBar = HealthBar(10, 10, player.health, player.max_health) 
enemy: Soldier = Soldier("enemy", 500, 250, 3, 5, 20, 0)
enemy_group.add(enemy)
enemy2: Soldier = Soldier("enemy", 700, 250, 3, 5, 20, 0)
enemy_group.add(enemy2)

running: bool = True
while running:
    clock.tick(FPS)

    draw_bg()
    # draw health bar
    health_bar.draw(screen, player.health)
    # Show player stats
    draw_text(f"Health: {player.health}", font, RED, 10, 10)
    draw_text(f"Ammo: {player.ammo}", font, RED, 10, 40)
    draw_text(f"Grenade: {player.grenade}", font, RED, 10, 70)  
    for x in range(player.grenade):
        screen.blit(grenade_img, (130 + (x * 15), 70))

    player.update()
    player.draw(screen)
    for enemy in enemy_group:
        enemy.draw(screen)
        enemy.update()

    # update and draw groups
    bullet_group.update(player, enemy_group)
    grenade_group.update(player, enemy_group, explosion_group)
    explosion_group.update()
    item_boxes_group.update(player)
    bullet_group.draw(screen)
    grenade_group.draw(screen)
    explosion_group.draw(screen)
    item_boxes_group.draw(screen)

    # update player actions
    if player.alives:
        if shoot:
            player.shoot(bullet_group, bullet_img)

        # throw grenade
        elif grenade and grenade_thrown == False and player.grenade > 0:
            grenade = Grenade(
                player.rect.centerx + 0.5 * player.rect.size[0] * player.direction,
                player.rect.top,
                player.direction,
                grenade_img,
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
