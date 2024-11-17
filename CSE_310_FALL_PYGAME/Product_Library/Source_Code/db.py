import sqlite3
import pygame
from player import Player
from enemy import Enemy
from platform import Platform
 
CONNECTION = sqlite3.connect('save_file.db')

CURSOR = CONNECTION.cursor()

def create_save(player: Player, enemies: list[Enemy], platforms: list[Platform]) -> None:
    """ Create a save file"""

    # Create Player Table
    player_save = """CREATE TABLE IF NOT EXISTS
    player(player_id VARCHAR PRIMARY KEY, level INTEGER, health INTEGER)"""
    CURSOR.execute(player_save)

    # Create enemy table
    enemy_save = """CREATE TABLE IF NOT EXISTS
    enemies(enemy_id INTEGER PRIMARY KEY, location_x INTEGER, location_y INTEGER)"""
    CURSOR.execute(enemy_save)

    # Create platform table
    platform_save = """CREATE TABLE IF NOT EXISTS
    platforms(platform_id INTEGER, location_x INTEGER, location_y INTEGER, width INTEGER, height INTEGER)"""
    CURSOR.execute(platform_save)

    # Add to player
    CURSOR.execute("""INSERT INTO player (player_id, level, health) VALUES (?, ?, ?)""",
                   (1, player.level, player.health))
    
    # Add to enemies
    for count, enemy in enumerate(enemies, start=1):
        CURSOR.execute("""INSERT INTO enemies (enemy_id, location_x, location_y) VALUES (?, ?, ?)""",
                       (count, enemy.rect.x, enemy.rect.y))
           
    # Add to platforms    
    for count, platform in enumerate(platforms, start=1):
        CURSOR.execute("""INSERT INTO platforms (platform_id, location_x, location_y, width, height) VALUES (?, ?, ?, ?, ?)""",
                       (count, platform.rect.x, platform.rect.y, platform.width, platform.height))

def load_player_save() -> Player:
    """Returns a Player object with attributes from 
    the save file."""

    CURSOR.execute('SELECT * FROM player')
    player_numbers = CURSOR.fetchall()

    return Player(player_numbers[0][1], player_numbers[0][2])

def load_enemies_save() -> list[Enemy]:
    """Receives a tuple from the save file and returns a list of Enemy objects."""

    enemy_list = []

    CURSOR.execute('SELECT * FROM enemies')
    enemies = CURSOR.fetchall()

    for enemy in enemies:
        new_enemy = Enemy()  # Adjust as needed to set a default or variable image

        new_enemy.set_xy(enemy[3], enemy[4])  # Assuming `enemy[2]` is `location_x` and `enemy[3]` is `location_y`
        enemy_list.append(new_enemy)

    return enemy_list

def load_platforms_save() -> list[Platform]:
    """Receives a tuple from the save file and returns 
    a list of Platform objects."""
    
    platforms = []  # Initialize as a list, not a tuple
    count = -1

    CURSOR.execute('SELECT * FROM platforms')
    platforms_data = CURSOR.fetchall()

    for platform in platforms_data:
        count += 1
        # Assuming platform columns are (platform_id, location_x, location_y, width, height)
        new_platform = Platform(platform[1], platform[2], platform[3], platform[4])
        platforms.append(new_platform)

    return platforms

def delete_save():
    """Deletes the tables of a save file."""
    try:
        # Drop the player table
        CURSOR.execute("DROP TABLE IF EXISTS player")

        # Drop the enemies table
        CURSOR.execute("DROP TABLE IF EXISTS enemies")

        # Drop the platforms table
        CURSOR.execute("DROP TABLE IF EXISTS platforms")

        # Commit the changes
        CONNECTION.commit()
        print("Save file deleted successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while deleting the save file: {e}")