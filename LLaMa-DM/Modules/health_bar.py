import pygame

class Health_Bar():
    def __init__(self,x, y):
        self.x = x
        self.y = y
        self.width = 150
        self.height = 20
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = (255, 0, 0)

    def mod_len(self, damage: int, mod_type: bool):
        if mod_type == True:
            self.width += damage
        else: 
            self.width -= damage