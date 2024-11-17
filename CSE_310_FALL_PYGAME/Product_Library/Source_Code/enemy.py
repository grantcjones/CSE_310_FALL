import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, player_image):
        super().__init__()
        self.image = pygame.image.load(player_image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (400, 500)
        self.direction = True  # Start moving in one direction (e.g., right)
        self.speed = 2         # Set speed of movement

    def patrol(self):
        # Switch direction when reaching a boundary or every time `patrol` is called
        if self.direction:
            self.rect.x += self.speed  # Move right
        else:
            self.rect.x -= self.speed  # Move left

        # Toggle direction when reaching a boundary (you can set custom boundaries here)
        if self.rect.right >= 999:  # Right boundary
            self.image = pygame.image.load("Product_Library/Source_Code/art/enemy_frame1_False.png")
            self.direction = False

        elif self.rect.left <= 0:   # Left boundary
            self.image = pygame.image.load("Product_Library/Source_Code/art/enemy_frame1_True.png")
            self.direction = True
