import pygame

from health_bar import HealthBar
from item_box import ItemBox
from settings import *
from soldiers import Soldier
from decoraters import Decorator, Water, Exit


class World:
    def __init__(self, data: list[list[int]] | None = None) -> None:
        self.data: list[list[int]] = data if data is not None else [[-1 for _ in range(COLS)] for _ in range(ROWS)]
        self.obstacle_list: list[tuple[pygame.Surface, pygame.Rect]] = []
        self.img_list: list[pygame.Surface] = []

        for tile_id in range(TILE_TYPES):
            img: pygame.Surface = pygame.image.load(f"img/tile/{tile_id}.png")
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            self.img_list.append(img)

        self.enemy_group: pygame.sprite.Group = pygame.sprite.Group()
        self.item_boxes_group: pygame.sprite.Group = pygame.sprite.Group()

        self.bullet_img: pygame.surface.Surface = pygame.image.load("img/icons/bullet.png").convert_alpha()
        self.grenade_img: pygame.surface.Surface = pygame.image.load("img/icons/grenade.png").convert_alpha()
        self.health_box_img: pygame.surface.Surface = pygame.image.load("img/icons/health_box.png").convert_alpha()
        self.ammo_box_img: pygame.surface.Surface = pygame.image.load("img/icons/ammo_box.png").convert_alpha()
        self.grenade_box_img: pygame.surface.Surface = pygame.image.load("img/icons/grenade_box.png").convert_alpha()

        self.item_boxes: dict[str, pygame.surface.Surface] = {
            "Health": self.health_box_img,
            "Ammo": self.ammo_box_img,
            "Grenade": self.grenade_box_img,
        }

        self.player: Soldier | None = None
        self.health_bar: HealthBar | None = None

        # create sprite groups for water, decoration, and exit
        self.water_group: pygame.sprite.Group = pygame.sprite.Group()
        self.decorator_group: pygame.sprite.Group = pygame.sprite.Group()
        self.exit_group: pygame.sprite.Group = pygame.sprite.Group()

    def process_data(self, data: list[list[int]]) -> tuple[Soldier, HealthBar]:
        self.obstacle_list = []
        self.enemy_group = pygame.sprite.Group()
        self.item_boxes_group = pygame.sprite.Group()
        self.player = None
        self.health_bar = None

        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile < 0:
                    continue

                if tile < len(self.img_list):
                    img: pygame.Surface = self.img_list[tile]
                    img_rect: pygame.Rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data: tuple[pygame.Surface, pygame.Rect] = (img, img_rect)

                    if 0 <= tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif 9 <= tile <= 10: # water
                        water: Water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        self.water_group.add(water)
                    elif 11 <= tile <= 14: # decoration
                        decorator: Decorator = Decorator(img, x * TILE_SIZE, y * TILE_SIZE)
                        self.decorator_group.add(decorator)
                    elif tile == 15:
                        self.player = Soldier("player", x * TILE_SIZE, y * TILE_SIZE, 1.65, 5, 20, 5)
                        self.health_bar = HealthBar(10, 10, self.player.health, self.player.max_health)
                    elif tile == 16:
                        enemy: Soldier = Soldier("enemy", x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 20, 0)
                        self.enemy_group.add(enemy)
                    elif tile == 17:
                        item_box: ItemBox = ItemBox("Ammo", x * TILE_SIZE, y * TILE_SIZE, self.ammo_box_img, self.item_boxes)
                        self.item_boxes_group.add(item_box)
                    elif tile == 18:
                        item_box = ItemBox("Grenade", x * TILE_SIZE, y * TILE_SIZE, self.grenade_box_img, self.item_boxes)
                        self.item_boxes_group.add(item_box)
                    elif tile == 19:
                        item_box = ItemBox("Health", x * TILE_SIZE, y * TILE_SIZE, self.health_box_img, self.item_boxes)
                        self.item_boxes_group.add(item_box)
                    elif tile == 20: # create exits
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        self.exit_group.add(exit)
        if self.player is None or self.health_bar is None:
            raise ValueError("Player start position not found in level data.")

        return self.player, self.health_bar

    def draw(self, window: pygame.surface.Surface) -> None:
        for tile in self.obstacle_list:
            window.blit(tile[0], tile[1])
        self.water_group.draw(window)
        self.decorator_group.draw(window)
        self.exit_group.draw(window)

    def update(self, player: Soldier) -> None:
        self.enemy_group.update()
        self.item_boxes_group.update(player)
        self.water_group.update()
        self.decorator_group.update()
        self.exit_group.update()
