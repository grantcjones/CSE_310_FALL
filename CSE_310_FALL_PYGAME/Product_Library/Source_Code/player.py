import pygame
from random import Random

class Player(pygame.sprite.Sprite):
    def __init__(self, health: int):
        super().__init__()
        self.image = pygame.image.load("Product_Library/Source_Code/art/player_frame1_True.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (500, 500)
        self.health = health
        self.level = int
        self.direction = True
        self.animation_True = [
            # Sprite frames facing right.
            "Product_Library/Source_Code/art/player_frame1_True.png",
            "Product_Library/Source_Code/art/player_frame2_True.png"
        ]
        self.animation_False = [
            # Sprite frames facing left.
            "Product_Library/Source_Code/art/player_frame1_False.png",
            "Product_Library/Source_Code/art/player_frame2_False.png"
        ]
        self.current_frame = 0
        self.frame_counter = 0
        self.last_update_time = pygame.time.get_ticks()
        self.frame_interval = 500  # Milliseconds for switching frames

    def update_frame(self):
        """Ensures the frame change is managed consistently, whether the player is facing True or False."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.frame_interval:
            self.last_update_time = current_time
            self.frame_counter = (self.frame_counter + 1) % 2

    def flip_True(self):
        """Faces the player sprite to the right."""

        if not self.direction:
            self.frame_counter = 0  # Reset frame counter when switching direction
        self.direction = True
        self.update_frame()
        self.image = pygame.image.load(self.animation_True[self.frame_counter])

    def flip_False(self):
        """Faces the player sprite to the left."""
        if self.direction:
            self.frame_counter = 0  # Reset frame counter when switching direction
        self.direction = False
        self.update_frame()
        self.image = pygame.image.load(self.animation_False[self.frame_counter])