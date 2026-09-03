import pygame

class SpriteSheet:
    def __init__(self, sheet) -> None:
        self.sheet = sheet

    def get_image(self, frame, width, heigth, scale, color):
        image = pygame.Surface((width, heigth)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame*width), 0, width, heigth))
        image = pygame.transform.scale(
                        image, (int(width * scale), int(heigth * scale))
                    ).convert_alpha()
        image.set_colorkey(color)
        return image