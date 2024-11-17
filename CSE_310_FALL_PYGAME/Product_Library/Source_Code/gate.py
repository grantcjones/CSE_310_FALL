import pygame

class Gate(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.image = pygame.image.load("Product_Library/Source_Code/art/Gate.png")
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)
        # self.rect.bottomleft = (int, int)

    def set_xy(self, x, y) -> None:
        """Used to set the gate's x/y coordinates."""
        self.rect.bottomleft = (x, y)
