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

# Player Action Variable
moving_left: bool = False
moving_right: bool = False
shoot: bool = False

#load images
#bullet
bullet_img: pygame.surface.Surface = pygame.image.load('img/icons/bullet.png').convert_alpha()

# Define color (Strict Tuple Hinting)
BG: tuple[int, int, int] = (144, 201, 120)
RED: tuple[int, int, int] = (255, 0, 0)


def draw_bg() -> None:  # Added return type hint
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (WIN_WIDTH, 300))


class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type: str, x: int, y: int, scale: int, speed: int, ammo: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.alives: bool = True
        self.char_type: str = char_type
        self.health: int = 100
        self.max_health: int = self.health
        self.speed: int = speed
        self.ammo: int = ammo
        self.start_ammo: int = ammo
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
                img: pygame.surface.Surface = pygame.image.load(f"img/{self.char_type}/{animation}/{i}.png").convert_alpha()
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
        #update cooldown
        if self.shoot_cooldown>0:
            self.shoot_cooldown-=1

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
        if self.shoot_cooldown==0 and self.ammo>0:
            self.shoot_cooldown = 20
            bullet: Bullet = Bullet(self.rect.centerx+int(0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            #reduse the ammo
            self.ammo-=1

    def update_animation(self) -> None:
        ANIMATION_COOLDOWN: float = 100
        self.image = self.animation_list[self.action][self.frame_index]
        
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = float(pygame.time.get_ticks())
            self.frame_index += 1
            
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action==3:
                self.frame_index= len(self.animation_list[self.action])-1
            else:
                self.frame_index = 0

    def check_alive(self):
        if self.health<=0:
            self.health=0
            self.speed=0
            self.alives = False
            self.update_action(3)

    def draw(self, window: pygame.surface.Surface) -> None:  # Added window type hint
        window.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def update_action(self, new_action: int) -> None:
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = float(pygame.time.get_ticks())

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: int, *groups: Any) -> None:
        super().__init__(*groups)
        self.speed: int = 10
        self.image: pygame.surface.Surface = bullet_img
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction: int = direction

    def update(self) -> None:
        #move bullets
        self.rect.x += (self.direction * self.speed)

        #check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > WIN_WIDTH:
            self.kill()

        # check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alives:
                player.health-=5
                print(f"Player: {player.health}")
                self.kill()
        if pygame.sprite.spritecollide(enemy, bullet_group, False):
            if enemy.alives:
                enemy.health-=25
                print(f"Enemy: {enemy.health}")
                self.kill()


#create sprite groups
bullet_group: pygame.sprite.Group = pygame.sprite.Group()


player: Soldier = Soldier("player", 200, 200, 3, 5, 30)
enemy: Soldier = Soldier("enemy", 400, 200, 3, 5, 20)

running: bool = True
while running:
    clock.tick(FPS)

    draw_bg()

    enemy.draw(screen)
    enemy.update()
    player.update()
    player.draw(screen)

    #update and draw groups
    bullet_group.update()
    bullet_group.draw(screen)

    #update player actions
    if player.alives:
        if shoot:
            player.shoot()
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

    pygame.display.update()

pygame.quit()
sys.exit()
