#--------------------------------------------------------------------------------------------------------------
#   Dependencies
#--------------------------------------------------------------------------------------------------------------

#------------------
#-   Libraries     -
#------------------

# import random
# import json
# import ollama
import pygame
# import textwrap
import sys
pygame.init()

#------------------
#-   Constants     -
#------------------
SCREEN_WIDTH, SCREEN_HEIGHT = (1000, 600)
BACKGROUND = pygame.transform.scale((pygame.image.load('Art/dungeon_wall.png')), (SCREEN_WIDTH, SCREEN_HEIGHT))
FONT = pygame.font.Font(None, 38)
#------------------
#-   Entities     -
#------------------
from Modules.entities import Entity, Enemy, Player

#------------------
#- Loading Screen -
#------------------
from Modules.loading import LoadingScreen
loading = LoadingScreen()

#------------------
#-       AI       -
#------------------
from Modules.ai import AI
ai = AI()

#------------------
#-  Simplicities  -
#------------------
from Modules.simplify import wait, clear, show_cursor, hide_cursor

#------------------
#-    Combat      -
#------------------
from Modules.combat import start_combat, turn

#--------------------------------------------------------------------------------------------------------------
#   Decision Trees
#--------------------------------------------------------------------------------------------------------------
    #! Not currently implemented
opening_decisions = {
    'village':[
                'You approach a village.',                      # Header
                'Will you like to enter the village?'           # Question
            ],
    'door':[
                'You approach a door',                          # Header
                'Would you you like to go through the door?'    # Question
            ],
    'dungeon':[
                'You approach a dungeon entrance',              # Header
                'Step into the dungeon entrance?'               # Question
            ],
}

#--------------------------------------------------------------------------------------------------------------
#   Functions
#--------------------------------------------------------------------------------------------------------------

def wrap_text(text, font, max_width):
    """Wrap text to fit within a given pixel width."""
    lines = []
    words = text.split(' ')  # Split text into words
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        # Measure the width of the test line
        line_width = font.size(test_line)[0]
        if line_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())  # Save the current line
            current_line = word + " "  # Start a new line

    # Add the last line
    if current_line:
        lines.append(current_line.strip())

    return lines

def get_fitting_font(text, font_path, max_width, max_height, initial_size=32):
    """Ensures text fits within its container."""
    font_size = initial_size
    while font_size > 10:  # Minimum readable size
        font = pygame.font.Font(font_path, font_size)
        wrapped_lines = wrap_text(text, font, max_width)
        total_height = len(wrapped_lines) * font.get_linesize()
        if total_height <= max_height:
            return font, wrapped_lines
        font_size -= 2  # Decrease font size
    return pygame.font.Font(font_path, 10), wrap_text(text, pygame.font.Font(font_path, 10), max_width)

# def test_AI():
#     for i in range(10):
#         clear()
#         options = [
#            'proceed',
#            'turn back',
#            'elaborate'
#         ]
#         situation = random.choice(list(opening_decisions.keys()))
#         user_input = ai.ask(opening_decisions[situation][1], options)
#     print("Finished testing")

def run():
    pygame.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Window")
    clock = pygame.time.Clock()

    running = True

    # Initial init of entities
    player = Player()
    enemy = Enemy('easy')

    count = 0
    turn_order = player
    outcome = ""
    # Output container
    output_rect = pygame.Rect(0, 335, SCREEN_WIDTH, SCREEN_HEIGHT - 200)
    font, wrapped_lines = get_fitting_font(outcome, None, SCREEN_WIDTH, output_rect.height)

    while running:
        
        # Update the display
        pygame.display.flip()
        clock.tick(60)  # Limit frame rate

        # First init of interaction button. Change turn_button_txt based on game state/event
        turn_button = pygame.Rect(200, 500, 150, 60)
        turn_button_txt = "Next Turn"

        # Draws background
        screen.blit(BACKGROUND, (0, 0))
                                                       
        # Renders turn description and wraps it
        pygame.draw.rect(screen, (0, 0, 0), output_rect)
        wrapped_lines = wrap_text(outcome, FONT, SCREEN_WIDTH)
        y_offset = output_rect.top + 10
        for line in wrapped_lines:
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (output_rect.left + 10, y_offset))
            y_offset += font.get_linesize()

        # Handles enemy render and Enemy Death Event
        if enemy.health > 0: # Combat state if enemy is alive
            enemy_health_txt = FONT.render(f"Enemy HP: {enemy.health}", True, (255, 0, 0))
            enemy_health_txt_rect = enemy_health_txt.get_rect(center = (800, 25))

            screen.blit(enemy.image, enemy.rect)  
            screen.blit(enemy_health_txt, enemy_health_txt_rect)

            pygame.draw.rect(screen, (225, 0, 0), turn_button)
            text_button_surface = FONT.render(turn_button_txt, True, (100, 100, 100))
            text_turn_button = text_button_surface.get_rect(center = turn_button.center)
            screen.blit(text_button_surface, text_turn_button)
        else: # Movement state if enemy is dead
            exit_txt = FONT.render(f"<- 'a' Exit", True, (255, 0, 0))
            continue_txt = FONT.render(f"'d' Continue ->", True, (255, 0, 0))

            screen.blit(exit_txt, exit_txt.get_rect(center = (100, 200)))
            screen.blit(continue_txt, continue_txt.get_rect(center = (900, 200)))
            count += 1

            keys = pygame.key.get_pressed()

            """If a player wishes to continue, they will move to the far right side
            of the screen. If they wish to exit, they can either click the window 
            exit button or move to the far left of the screen."""
            if keys[pygame.K_a]: # Moves player left
                player.rect.x -= 1.9
            elif keys[pygame.K_d]: # Moves player right
                player.rect.x += 1.5

            if player.rect.x <= 0:
                sys.exit()
            elif player.rect.x >= SCREEN_WIDTH:
                player.rect.topleft = (400, 250) # Returns player to starting postion
                outcome = '' # Clears description
                enemy = Enemy('easy')

        # Handles player render and Death Event
        if player.health > 0:
            player_health_txt = FONT.render(f"Player HP: {player.health}", True, (255, 0, 0))
            player_health_txt_rect = player_health_txt.get_rect(center = (200, 25))

            screen.blit(player.image, player.rect)
            screen.blit(player_health_txt, player_health_txt_rect)
        else:
            turn_button_txt = "Continue"

            pygame.draw.rect(screen, (225, 0, 0), turn_button)
            text_button_surface = FONT.render(turn_button_txt, True, (100, 100, 100))
            text_turn_button = text_button_surface.get_rect(center = turn_button.center)
            screen.blit(text_button_surface, text_turn_button)
            
            outcome = ("You have died. Do you wish to continue?")

        # Handle exit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Check for mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if turn_button.collidepoint(event.pos):  # Check if click is inside button
                    if turn_order == player:
                        outcome = turn(player, enemy)
                        turn_order = enemy
                    else:
                        outcome = turn(enemy, player)
                        turn_order = player

def main():
    try:
        pygame.mixer.init()
    except pygame.error as e:
        print(f"Error initializing Pygame mixer: {e}")
        sys.exit(1)

    # Initialize Music
    pygame.mixer.music.load("Audio/8-bit-dungeon-251388.mp3")
    pygame.mixer.music.play(-1)

    run()

if __name__ == '__main__':
    main()