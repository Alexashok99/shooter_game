import sys
import pygame
import os

# Constant
WIN_HIGHT: int = 500
WIN_WIDTH: int = 800

pygame.init()

# pygame setup
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()
FPS: int = 60

GRAVITY: float = 0.75

# Player Action Veriable
moving_left: bool = False
moving_right: bool = False

# Define color
BG: tuple = (144, 201, 120)
RED: tuple = (255, 0, 0)


def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (WIN_WIDTH, 300))


class Sholdier(pygame.sprite.Sprite):
    def __init__(self, char_type, x: int, y: int, scale: int, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alives: bool = True
        self.char_type: str = char_type
        self.spped: int = speed
        self.direction: int = 1
        self.vel_y: int = 0
        self.jump: bool = False
        self.in_air: bool = True
        self.flip: bool = False
        self.animation_list: list = []
        self.frame_index: int = 0
        self.action: int = 0
        self.update_time: float = pygame.time.get_ticks()

        # load all images for the player
        animation_type: list = ["Idle", "Run", "Jump"]
        for animation in animation_type:
            # reset temporary list of images
            temp_list: list = []
            # coun number of files in the folder
            num_of_frames = len(os.listdir(f"img/{self.char_type}/{animation}"))
            for i in range(num_of_frames):
                img = pygame.image.load(f"img/{self.char_type}/{animation}/{i}.png")
                img = pygame.transform.scale(
                    img, (int(img.get_width() * scale), int(img.get_width() * scale))
                )
                temp_list.append(img)

            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left: bool, moving_right: bool):
        # Reset movement var
        dx: int = 0
        dy: int = 0
        # assign movement var
        if moving_left:
            dx = -self.spped
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.spped
            self.flip = False
            self.direction = 1

        # jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # applying gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        # check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        # update rect position
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN: float = 100
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def draw(self, window):
        window.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def update_action(self, new_action: int):
        # check if the new action is differnt to previous on
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


player: Sholdier = Sholdier("player", 200, 200, 3, 5)
enemy: Sholdier = Sholdier("enemy", 400, 200, 3, 5)


running: bool = True
while running:
    clock.tick(FPS)  # limits FPS to 60

    draw_bg()

    enemy.draw(screen)
    player.update_animation()
    player.draw(screen)
    # Player Alive
    if player.alives:
        # update player action
        if player.in_air:
            player.update_action(2)  # 2: Jump
        elif moving_left or moving_right:
            player.update_action(1)  # 1: run
        else:
            player.update_action(0)  # 0: Idle
        player.move(moving_left, moving_right)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Key Press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w and player.alives:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                running = False
        # Key Release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()


pygame.quit()
sys.exit()
