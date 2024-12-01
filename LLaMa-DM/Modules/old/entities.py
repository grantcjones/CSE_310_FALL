#--------------------------------------------------------------------------------------------------------------
#   Dependancies
#--------------------------------------------------------------------------------------------------------------

import json
import random
from Modules.weapon import Weapon

#--------------------------------------------------------------------------------------------------------------
#   Entity
#--------------------------------------------------------------------------------------------------------------

class Entity:
    def __init__(self, max_health:int=20):
        self.health = max_health
        self.max_health = max_health
        self.dead = False
        self.hit_chance = 60

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
        "Outputs damage for the entity to inflict"
        damage = self.max_health/10
        return damage

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
        health = int # Default health
        if difficulty == 'easy':
            health = random.randint(1, 10)
        if difficulty == 'med':
            health = random.randint(10, 20)
        else:
            health = random.randint(20, 30)
        super().__init__(health)
        self.enemy_data = random.choice(ENEMIES[f'{difficulty}_dif'])
        self.name = 'placeholder'

    def deal_damge(self) -> int:
        return super().deal_damage()

#--------------------------------------------------------------------------------------------------------------
#   Player
#--------------------------------------------------------------------------------------------------------------

class Player(Entity):
    def __init__(self):
        super().__init__(20)
        self.equipped = Weapon('Gregorator', 5)
        self.hit_chance = 80
    
    def equip(self, name:str, damage:float):
        "Equips a weapon onto the player."
        self.equipped = Weapon(name, damage)