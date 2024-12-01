#--------------------------------------------------------------------------------------------------------------
#   Dependancies
#--------------------------------------------------------------------------------------------------------------

import json
import random
import pygame
from Modules.weapon import Weapon
from Modules.health_bar import Health_Bar

#--------------------------------------------------------------------------------------------------------------
#   Entity
#--------------------------------------------------------------------------------------------------------------

class Entity(pygame.sprite.Sprite):
    def __init__(self, max_health:int=20):
        self.health = max_health
        self.max_health = max_health
        self.dead = False
        self.hit_chance = 60
        self.name = str
        self.health_bar = Health_Bar(0, 0)
        

    def take_damage(self, damage:int):
        "Damages the entity."
        self.health -= damage
        if self.health - damage <= 0:
            self.dead = True

    def roll_hit(self) -> bool:
        "Outputs success/failure of a hit"
        chance = random.random() * 100
        
        if chance < self.hit_chance:
            return True
        else:
            return False

    def deal_damage(self) -> int:
        return 2
#--------------------------------------------------------------------------------------------------------------
#   Enemy
#--------------------------------------------------------------------------------------------------------------

# Enemy data
with open('data/enemies.json', 'r') as file:
    enemy_data = json.load(file)
ENEMIES = {
    'easy_dif':enemy_data['enemies']['easy'],
    'med_dif':enemy_data['enemies']['medium'],
    'hard_dif':enemy_data['enemies']['hard']
}  

# Enemy class
class Enemy(Entity):
    def __init__(self, difficulty:str='easy'):
        #TODO CHANCE DIFFICULTY TO NUMBER
        # self.image = pygame.image.load('Art/enemy_frame1_False.png')
        self.image = pygame.transform.scale((pygame.image.load('Art/enemy_frame1_False.png')) , (84, 84))

        self.rect = self.image.get_rect()
        self.rect.topleft = (500, 250)
        self.health = int # Default health
        if difficulty == 'easy':
            self.health = random.randint(1, 10)
        if difficulty == 'med':
            self.health = random.randint(10, 20)
        else:
            self.health = random.randint(20, 30)
        super().__init__(self.health)
        self.enemy_data = random.choice(ENEMIES[f'{difficulty}_dif'])
        self.damage = 2
        self.name = 'Enemy'

    def deal_damge(self) -> int:
        return 2

#--------------------------------------------------------------------------------------------------------------
#   Player
#--------------------------------------------------------------------------------------------------------------

class Player(Entity):
    def __init__(self):
        super().__init__(20)
        # self.image = pygame.image.load('Art/player_frame1_True.png')
        self.image = pygame.transform.scale((pygame.image.load('Art/player_frame1_True.png')) , (54, 84))
        self.rect = self.image.get_rect()
        self.rect.topleft = (400, 250)
        self.equipped = Weapon('Gregorator', 10)
        self.hit_chance = 80
        self.name = 'player'
    
    def equip(self, name:str, damage:float):
        "Equips a weapon onto the player."
        self.equipped = Weapon(name, damage)

    def deal_damage(self):
        return self.equipped.damage