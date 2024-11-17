import pygame
import sys
import random
import math
from player import Player
from enemy import Enemy
from platform import Platform
from gate import Gate

from db import create_save
from db import load_player_save
from db import load_enemies_save
from db import load_platforms_save

pygame.init()

try:
    pygame.mixer.init()
except pygame.error as e:
    print(f"Error initializing Pygame mixer: {e}")
    sys.exit(1)

# Constants
BACKGROUND_IMAGES = [
    'Product_Library/Source_Code/art/background_1.png',
    'Product_Library/Source_Code/art/background_2.png',
    'Product_Library/Source_Code/art/background_3.png',
    'Product_Library/Source_Code/art/background_4.png',
    'Product_Library/Source_Code/art/background_5.png',
    'Product_Library/Source_Code/art/background_6.png',
    'Product_Library/Source_Code/art/background_7.png',
    'Product_Library/Source_Code/art/background_8.png',
    'Product_Library/Source_Code/art/background_9.png',
    'Product_Library/Source_Code/art/background_10.png'
]
# PLAYER_IMAGE = 'Product_Library/Source_Code/art/player.png'
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600

# Player movement settings
move_speed = 4
jump_height = 25
gravity = 1
velocity_y = 0
is_jumping = False

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Fonts
font = pygame.font.Font(None, 50)

# Save loading
def call_save():
    player = load_player_save()

    enemies = load_enemies_save

    platforms = load_platforms_save

    return [player, enemies, platforms]

# Menus
    # Menu options
options = ["New Game", "Load Game", "Exit"]
buttons = []

    # Create buttons as rects
for i, option in enumerate(options):
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 150 + i * 100, 200, 50)
    buttons.append((button_rect, option))

def draw_menu():
    """Draw the menu options."""

    menu_bg = pygame.image.load('Product_Library/Source_Code/art/dungeon_wall.png')
    screen.blit(pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
    for button, text in buttons:
        # Draw button
        pygame.draw.rect(screen, (200, 200, 200), button)
        # Render text
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=button.center)
        screen.blit(text_surface, text_rect)

def handle_click(pos):
    """Handle mouse click on the menu."""
    background_image = load_random_background()

    for button, text in buttons:
        if button.collidepoint(pos):
            if text == "New Game":
                print("New Game selected!")
                # Load initial background image
                

                # Generate platforms and exit
                num_platforms = random.randint(6, 9)
                platforms = generate_platforms(num_platforms, pygame.Rect(0, 0, 50, 50))  # Dummy exit rect for initial generation
                exit_rect = generate_exit(platforms)

                # Load player and set starting position randomly on a platform
                player = Player(10)
                platforms_list = list(platforms)
                random_platform = random.choice(platforms_list)
                player.rect.midbottom = (random_platform.rect.centerx, random_platform.rect.top)
                enemies = []

                run(player, enemies, platforms, background_image)

            elif text == "Load Game":
                print("Load Game selected!")
                save_data = call_save()

                player = save_data[0]

                enemies = save_data[1]

                platforms_list = save_data[2]
                exit_rect = generate_exit(platforms_list)
                run(player, enemies, platforms_list, exit_rect, background_image)

            elif text == "Exit":
                print("Exiting game...")
                pygame.quit()
                sys.exit()


# Function to load a random background image
def load_random_background():
    background_image_path = random.choice(BACKGROUND_IMAGES)
    try:
        background_image = pygame.image.load(background_image_path)
        return pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except pygame.error as e:
        print(f"Error loading background image: {e}")
        sys.exit(1)

# Constants for minimum and maximum gaps between platforms
MIN_GAP_X = 100  # minimum gap in the x direction
MAX_GAP_X = 400  # maximum gap in the x direction
MIN_GAP_Y = 80   # minimum gap in the y direction
MAX_GAP_Y = 300  # maximum gap in the y direction

# Modified generate_platforms function to ensure gaps between platforms
def generate_platforms(num_platforms, exit_rect):
    platforms = pygame.sprite.Group()
    last_platform_rect = None

    for _ in range(num_platforms):
        attempt = 0
        while attempt < 10:
            width = random.randint(80, 200)
            height = 20
            if last_platform_rect:
                # Set x and y based on the last platform to maintain gaps
                x = last_platform_rect.right + random.randint(MIN_GAP_X, MAX_GAP_X)
                y = last_platform_rect.top + random.randint(-MAX_GAP_Y, MAX_GAP_Y)
                # Ensure new platform doesn't go off-screen
                if x + width > SCREEN_WIDTH:
                    x = random.randint(0, SCREEN_WIDTH - width)
                if y < 50 or y > SCREEN_HEIGHT - height - 50:
                    y = random.randint(50, SCREEN_HEIGHT - height - 50)
            else:
                # Position first platform randomly within screen bounds
                x = random.randint(0, SCREEN_WIDTH - width)
                y = random.randint(50, SCREEN_HEIGHT - height - 50)

            new_platform = Platform(x, y, width, height)

            # Ensure no overlap with existing platforms and no collision with exit
            if not any(platform.rect.colliderect(new_platform.rect) for platform in platforms) and \
               not new_platform.rect.colliderect(exit_rect):
                platforms.add(new_platform)
                last_platform_rect = new_platform.rect  # Update last platform position
                break
            attempt += 1
    return platforms

# Function to generate exit rectangle
def generate_exit(platforms):
    while True:
        exit_width = 50
        exit_height = 50
        x = random.randint(0, SCREEN_WIDTH - exit_width)
        y = random.randint(50, SCREEN_HEIGHT - exit_height - 50)

        exit_rect = Gate(x, y)

        # Check if the exit is on a platform
        if any(platform.rect.colliderect(exit_rect) for platform in platforms):
            return exit_rect

# Gameloop function
def run(player, enemies, platforms, background_start):
    #! Enemies are currently not implemented into the game loop, and will be developed in a different branch
    num_platforms = len(platforms)
    # background = pygame.image.load(background_start)
    clock = pygame.time.Clock()

    # Game loop
    while True:

        pygame.event.pump()

        # Frame rate control
        clock.tick(60)  # Limit to 60 frames per second

        # Player input handling
        keys = pygame.key.get_pressed()
            
        # Move Left
        if keys[pygame.K_a] and player.rect.left > 0:
            player.flip_False()
            player.rect.x -= 8
        
            # Move Right
        if keys[pygame.K_d] and player.rect.right < 1000:
            player.flip_True()
            player.rect.x += 8

            # Jump
        if keys[pygame.K_SPACE] and not is_jumping:
            is_jumping = True
            velocity_y = -jump_height

        # Apply gravity or jumping
        player.rect.y += velocity_y
        velocity_y += gravity if is_jumping else 0

        # Collision detection with platforms
        on_platform = False
        for platform in platforms:
            if player.rect.colliderect(platform.rect):
                if velocity_y > 0:  # Player is falling
                    player.rect.bottom = platform.rect.top
                    velocity_y = 0
                    is_jumping = False
                    on_platform = True
                    break

        # Apply gravity only if not on any platform
        if not on_platform and player.rect.bottom < SCREEN_HEIGHT:
            velocity_y += gravity

        # Check for level exit
        if player.rect.colliderect(exit_rect):
            # Load new level
            background_image = load_random_background()
            platforms = generate_platforms(num_platforms, exit_rect)  # Regenerate platforms
            exit_rect = generate_exit(platforms)  # Generate new exit
            
            # Convert platforms group to a list and respawn player on a new platform
            platforms_list = list(platforms)
            random_platform = random.choice(platforms_list) if platforms_list else None  # Check if there are platforms
            if random_platform:
                player.rect.midbottom = (random_platform.rect.centerx, random_platform.rect.top)

            # Check if the player has fallen past the bottom of the screen
        if player.rect.top >= SCREEN_HEIGHT:
            # Convert platforms group to a list and respawn player on a new platform
            platforms_list = list(platforms)
            random_platform = random.choice(platforms_list) if platforms_list else None  # Check if there are platforms
            if random_platform:
                # Respawn the player on the selected platform
                player.rect.midbottom = (random_platform.rect.centerx, random_platform.rect.top)
                # Reset vertical velocity to prevent immediate falling
                velocity_y = 0
                is_jumping = False

        # Exit condition
        if keys[pygame.K_ESCAPE]:
            break

        screen.blit(background_image, (0,0))
        platforms.draw(screen)
        screen.blit(exit_rect.image, exit_rect.rect)  # Draw exit rectangle
        screen.blit(player.image, player.rect)  # Draw player on the screen
        pygame.display.flip()  # Update the display

        clock.tick(60)

def main():
    # Frame rate control

    running = True
    while running:
        draw_menu()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    handle_click(event.pos)

    pygame.quit()

if __name__ == '__main__':
    main()