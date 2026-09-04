import csv
import sys
from typing import Any

import pygame

from class_based.grenade import Grenade
from class_based.settings import *
from class_based.worlds import World

pygame.init()

screen: pygame.surface.Surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Shooter")
clock: pygame.time.Clock = pygame.time.Clock()

moving_left: bool = False
moving_right: bool = False
shoot: bool = False
grenade: bool = False
grenade_thrown: bool = False

level: int = 1
font: pygame.font.Font = pygame.font.SysFont("Consolas", 20)


def draw_text(
    text: str,
    font: pygame.font.Font,
    text_col: tuple[int, int, int],
    x: int,
    y: int,
) -> None:
    img: pygame.surface.Surface = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_bg() -> None:
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (WIN_WIDTH, 300))


world_data: list[list[int]] = [[-1 for _ in range(COLS)] for _ in range(ROWS)]
with open(f"level{level}_data.csv", newline="") as csvfile:
    reader: Any = csv.reader(csvfile, delimiter=",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            if 0 <= x < ROWS and 0 <= y < COLS:
                world_data[x][y] = int(tile)

world = World(world_data)
player, health_bar = world.process_data(world_data)

bullet_group: pygame.sprite.Group = pygame.sprite.Group()
grenade_group: pygame.sprite.Group = pygame.sprite.Group()
explosion_group: pygame.sprite.Group = pygame.sprite.Group()

running: bool = True
while running:
    clock.tick(FPS)

    draw_bg()
    world.draw(screen)
    world.update(player)
    health_bar.draw(screen, player.health)

    draw_text(f"Health: {player.health}", font, RED, 10, 10)
    draw_text(f"Ammo: {player.ammo}", font, RED, 10, 40)
    draw_text(f"Grenade: {player.grenade}", font, RED, 10, 70)
    for x in range(player.grenade):
        screen.blit(world.grenade_img, (130 + (x * 15), 70))

    player.update()
    player.draw(screen)
    for enemy in world.enemy_group:
        enemy.ai(screen, player, world.bullet_img, bullet_group)
        enemy.draw(screen)
        enemy.update()

    bullet_group.update(player, world.enemy_group)
    grenade_group.update(player, world.enemy_group, explosion_group)
    explosion_group.update()
    world.item_boxes_group.update(player)
    bullet_group.draw(screen)
    grenade_group.draw(screen)
    explosion_group.draw(screen)
    world.item_boxes_group.draw(screen)

    if player.alives:
        if shoot:
            player.shoot(bullet_group, world.bullet_img)
        elif grenade and not grenade_thrown and player.grenade > 0:
            grenade_obj = Grenade(
                player.rect.centerx + 0.5 * player.rect.size[0] * player.direction,
                player.rect.top,
                player.direction,
                world.grenade_img,
            )
            grenade_group.add(grenade_obj)
            player.grenade -= 1
            grenade_thrown = True

        if player.in_air:
            player.update_action(2)
        elif moving_left or moving_right:
            player.update_action(1)
        else:
            player.update_action(0)
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
