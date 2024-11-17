import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        
        # Load the platform image and scale it to the specified width and height
        original_image = pygame.image.load('Product_Library/Source_Code/art/platform.png').convert_alpha()  # Load with transparency support
        self.image = pygame.transform.scale(original_image, (width, height))
        
        # Set the rectangle for positioning
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        # Placeholder for future update logic, such as movement or interaction
        pass
