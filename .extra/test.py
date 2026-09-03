
import pygame, sys
from spritesheet import SpriteSheet


# Constant
WIN_HEIGHT: int = 500
WIN_WIDTH: int = 800

# Define color (Strict Tuple Hinting)
BG: tuple[int, int, int] = (50, 50, 50)
RED: tuple[int, int, int] = (255, 0, 0)
BLACK: tuple[int, int, int] = (0, 0, 0)
WHITE: tuple[int, int, int] = (255, 255, 255)

scale = 3

pygame.init()

# pygame setup
screen: pygame.surface.Surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("test")
clock: pygame.time.Clock = pygame.time.Clock()

sprite_sheet_image = pygame.image.load("doux.png").convert_alpha()

# img = pygame.transform.scale(
#                     sprite_sheet_image, (int(sprite_sheet_image.get_width() * scale), int(sprite_sheet_image.get_height() * scale))
#                 ).convert_alpha()

# def get_image(sheet, frame, width, heigth, scale, color):
#     image = pygame.Surface((width, heigth)).convert_alpha()
#     image.blit(sheet, (0, 0), ((frame*width), 0, width, heigth))
#     image = pygame.transform.scale(
#                     image, (int(width * scale), int(heigth * scale))
#                 ).convert_alpha()
#     image.set_colorkey(color)
#     return image

sprite_sheet = SpriteSheet(sprite_sheet_image)

frame_0 = sprite_sheet.get_image( 0, 24, 24, scale, BLACK)
frame_1 = sprite_sheet.get_image( 2, 24, 24, scale, color=
                                 BLACK)

running: bool = True
while running:
    clock.tick(60)
    screen.fill(BG)
    screen.blit(frame_0, (0,0))
    screen.blit(frame_1, (72,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    pygame.display.update()

pygame.quit()
sys.exit()
