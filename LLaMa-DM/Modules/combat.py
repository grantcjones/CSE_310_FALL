from Modules.entities import Entity, Enemy, Player
from Modules.ai import AI
ai = AI()

def start_combat(player:Player, enemy:Enemy=None) -> str:
    print(enemy)
    if enemy == None:
        enemy = Enemy()
    "Begins combat"
    print("Combat began")
    # print(enemy.health)
    while enemy.health > 0 or player.health > 0:
        # Player Attack
        if player.health > 0:
            turn(player, enemy)
        else:
            return 'You died.'
            break
        # Enemy attack
        if enemy.health > 0:
            turn(enemy, player)
        else:
            return f'{enemy.name} died.'
            break
    print("Combat finished")

def turn(attacker: Entity, defender: Entity):
    "Start a new combat turn"
    if attacker.roll_hit():
        damage_dealt = attacker.deal_damage()
        defender.take_damage(damage_dealt)
        if isinstance(attacker, Player):
            situation = f'You attacked {defender.name} for {damage_dealt} damage.'
        else:
            situation = f'{attacker.name} attacked you for {damage_dealt} damage.'
    else:
        if isinstance(attacker, Player):
            situation = f'You missed trying to hit {attacker.name}.'
        else:
            situation = f'{attacker.name} missed trying to hit you.'
    description = ai.describe_turn(situation)
    return (description)
    