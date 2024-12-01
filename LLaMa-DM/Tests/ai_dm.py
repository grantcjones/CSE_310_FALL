import ollama
import time
import random
import threading
import json
import sys

debug_mode = True

ai_votes = 3
ai_refresh_limit = 10

VERSION = 'llama3.2:latest'
EQUIPPED = {
    "name":"Death Bringer",
    "damage":5
}

player = {
    'name':'name',
    'max_health':50,
    'health':50
}



#--------------------------------------------------------------------------------------------------------------
#   0 - Clear screen, hide cursor, show cursor + bonus niceties
#--------------------------------------------------------------------------------------------------------------

def clear():
    print("\033[H\033[J")

def hide_cursor():
    sys.stdout.write("\033[?25l")

def show_cursor():
    sys.stdout.write("\033[?25h")

#--------------------------------------------------------------------------------------------------------------
#   1 - Loading Screen
#--------------------------------------------------------------------------------------------------------------

loading_thread = 0

has_stopped = True

def loading_screen(reason):
    global has_stopped
    global loading_thread

    # Set the thread ID, which allows it to be terminated with loading_thread = 0
    this_thread = threading.current_thread().ident
    loading_thread = this_thread
    
    # Initialize animation
    animation = ["\\", "|", "/", "-"]
    index = 0

    # And here we begin.
    while loading_thread == this_thread:
        clear()
        print(f"{reason.title()}... {animation[index]}")
        index = (index + 1) % len(animation)
        time.sleep(0.1)
    has_stopped = True

# The way start_loading works is by checking if start_loading is true. Meaning it is currently stopped. If it is, it starts it.

def start_loading(reason="Loading"):
    global has_stopped
    if has_stopped:
        # Hide Cursor + clear console
        hide_cursor()
        clear()

        has_stopped = False
        threading.Thread(target=loading_screen, args=(reason,)).start()

# The way stop_loading works is by stopping the loading screen with loading_thread = 0 and then waiting for the loading screen to set has_stopped to true. When this happens, the function stops. This stops the main thread until it's done, preventing multiple loading screens from running at once.

def stop_loading():
    global has_stopped
    global loading_thread

    loading_thread = 0

    while not has_stopped:
        time.sleep(0.05)

    #Unhide Cursor + clear console
    show_cursor()
    clear()
        
#--------------------------------------------------------------------------------------------------------------
#   2 - Intent Recognition
#--------------------------------------------------------------------------------------------------------------

# All of the default choices
basic_choices = ["check inventory/health"]

def find_intent(player_prompt, choices, context=None, basic_choice=True, debug=False):
    clear()
    # Check if context and enemy exist and print them.
    if context:
        print(f"{f'{context}\n' + f'\n{enemy['name']}: {enemy['health']}/{enemy['max_health']} HP'if enemy else f'{context}\n'}")

    # Check if the default choices are allowed in this instance. They are by default. If not, they're not added to the list of choices.
    choice_string = f", ".join(list(choices)) + ", " + f", ".join(list(basic_choices)) if basic_choice else ", ".join(choices)
    basic_string = f", ".join(list(basic_choices))

    # Print the choices to the player.
    print(f"------------------------------------------------------------------------\nOptions: {choice_string.title()}\n------------------------------------------------------------------------")
    userInput = input(player_prompt + " ")
    clear()

    intent_found = False
    refresh = 0
    while not intent_found and refresh < ai_refresh_limit:
        refresh += 1

        # Start generating the 5 interpretations to be weighed against each other
        start_loading("Reading intent")

        compiled_responses = ""
        for i in range(ai_votes):
            prompt = f"The player was asked the DIRECT question '{player_prompt}'. Match the intent of the player input '{userInput}' to ONE of the following EXACT phrases seperated by commas: {choice_string}. Keep in mind the player is stating what THEY are want to do RIGHT NOW. Output ONLY one EXACT matching phrase from the list. Give ONE sentence explaining your reasoning on a new line."
            analysis = ollama.generate(VERSION, prompt)['response']
            compiled_responses = compiled_responses + f"\n{analysis}\n---------------------------------------------------------------------"

        stop_loading()

        # Prompt the AI to pick the most common interpretation
        start_loading("Analyzing")

        prompt = f"Look at the following and ONLY output the most commonly picked choice, NOT any kind of reasoning, punctuation, or list: [\n{compiled_responses}]."
        compiled_vote = ollama.generate(VERSION, prompt)['response'].lower().strip(", .")

        stop_loading()

        if debug == True:
            start_loading("Generating debug")

            prompt = f"Make a tally for how many times each choice was picked and summarize why they were picked: [\n{compiled_responses}]. The responses are assumptions from AI intent detectors, and they all received the exact same user input. You're here to parse them."
            debug_output = ollama.generate(VERSION, prompt)['response'].lower().strip(", .")
                

            stop_loading()

            print(debug_output)
            time.sleep(5)
        # Return the result
        if compiled_vote in choice_string:
            if compiled_vote in basic_string:
                if "health" in compiled_vote or "inventory" in compiled_vote:
                    check_player_stats()
                    return compiled_vote
            else:
                intent_found = True
            
    if refresh >= ai_refresh_limit:
        print("Couldn't find intent")
    return compiled_vote

        
#--------------------------------------------------------------------------------------------------------------
#   3 - Enemy Description
#--------------------------------------------------------------------------------------------------------------

enemy = None
# This makes 
easy = "easy"
medium = "medium"
hard = "hard"


def describe_enemy(difficulty=easy):
    
    with open('data/enemies.json', 'r') as file:
        ENEMY_DATA = json.load(file)
        
    easy_diff = ENEMY_DATA['enemies']['easy']
    med_diff = ENEMY_DATA['enemies']['medium']
    hard_diff = ENEMY_DATA['enemies']['hard']

    #start_loading("Generating room")

    health = 0 # Just declaring this for later

    # Easy by default. Otherwise, it checks for "medium" and "hard".
    if difficulty == "easy":
        health = random.randint(10, 15)
        enemy_pick = enemy_pick = easy_diff[random.randint(0, len(easy_diff)-1)]
    if difficulty == "medium":
        enemy_pick = med_diff[random.randint(0, len(med_diff)-1)]
        health = random.randint(15, 20)
    elif difficulty == "hard":
        health = random.randint(20, 25)
        global enemy
        enemy_pick = hard_diff[random.randint(0, len(hard_diff)-1)]

    # Generate the description
    prompt = f"Create a SHORT description for an enemy described simply as \"{enemy_pick['name']}\" in a room described as \"{enemy_pick['room']}\" with a more flowery and foreboding atmosphere in just ONE sentence. INCLUDE the TYPE (wolf, golbin, robot, etc) of enemy and NAME them. Otherwise, take creative liberty. Do NOT explain your reasoning."
    stream = ollama.generate(VERSION, prompt, stream=True)
    output = ''
    context = []
    for chunk in stream:
        print(chunk['response'], end='', flush=True)
        output = output + chunk['response']
        try:
            context = chunk['context']
        except:
            ""


    

    # Extract the enemy's name
    prompt = f"Extract the name from: {output}. Do NOT explain your reasoning. ONLY output the name."
    name = ollama.generate(VERSION, prompt)['response'].strip(",.")

    global enemy
    enemy = {
        'name':name,
        'max_health':health,
        'health':health
    }

    #stop_loading()

    return output, name

#--------------------------------------------------------------------------------------------------------------
#   3 - Better Descriptions
#--------------------------------------------------------------------------------------------------------------

situation_context = []

def describe(base, stream=False, context=False):
    hide_cursor()
    prompt = f'Make a more descriptive but breif second person, dark fantasy (game genre) version of "{base}". It should be ONE sentence. Don\'t be so poetic it isn\'t clear what happened. Do not explain your reasoning or surround your response in quotes, as your response is given verbatim to the player.'
    global situation_context   
    if stream == True:
        output = ollama.generate(VERSION, prompt, stream=True, context=(situation_context if context == True else None))
    else:
        output = ollama.generate(VERSION, prompt, stream=True, context=(situation_context if context == True else None))
    return output

def elaborate(base):
    # hide_cursor()
    stream = describe(base, True, context=True)
    for chunk in stream:
        print(chunk['response'], end='', flush=True)
    # show_cursor()
    # time.sleep(0.1)
    

#--------------------------------------------------------------------------------------------------------------
#   4 - Menu Functions
#--------------------------------------------------------------------------------------------------------------

# Inventory and Health
def check_player_stats():
    print(f"""---------------------------------------------------------------------
Your health: {player['health']}/{player['max_health']}
---------------------------------------------------------------------""")
    input("Continue? ")

#--------------------------------------------------------------------------------------------------------------
#   4 - Game Loop
#--------------------------------------------------------------------------------------------------------------

# Combat loop

def enter_combat(difficulty=easy):
    # Start combat
    room, name = describe_enemy(difficulty)
    player_prompt = "What would you like to do?"
    choices = ["attack"]

    #Continue combat
    while enemy['health'] > 0 and player['health'] > 0:
        intent = find_intent(player_prompt, choices, room)
        #print(f"INTENT DETECTED AS [{intent}]")
        
        if "attack" in intent:
            #----------------------------
            #-      Player's turn       -    
            #----------------------------
            hide_cursor()
            hit_chance = random.random()
            if hit_chance < 0.7:
                enemy['health'] -= EQUIPPED['damage']
                elaborate(f"You hit {name} for {EQUIPPED['damage']} points of damage.")
            else:
                elaborate(f"You missed trying to hit {enemy['name']}.")
            
            print()
            for i in range(6):
                time.sleep(0.5)
                print(".", end='', flush=True)
            print()

            #----------------------------
            #-       Enemy's turn       -
            #----------------------------
            hit_chance = random.random()
            if hit_chance < 0.5:
                player['health'] -= EQUIPPED['damage']
                elaborate(f"{name} hit you for {EQUIPPED['damage']} damage.")
            else:
                elaborate(f"{name} missed trying to hit you.")
            print("\n")
            show_cursor()
            input("Continue? ")

    #----------------------------
    #-     Check for deaths     -
    #----------------------------

    if enemy['health'] <= 0:
        clear()
        time.sleep(1)
        elaborate(f"You killed {name}.")
        print("\n")
        input("Continue? ")
        if player['health'] > 0:
            return
    if player['health'] <= 0:
        clear()
        time.sleep(1)
        quit(f"You were killed by {name}.")
    time.sleep(0.1)
    
        

# Main Loop

def main():
    # Begin Everything
    player_prompt = "Would you like to begin?"
    context = "You approach a door."
    choices = ["begin game"]

    intent = find_intent(player_prompt, choices, context, basic_choice=False)
    if intent == "begin game":
        for i in range(3):
            enter_combat()
        for i in range(3):
            enter_combat(medium)
        for i in range(3):
            enter_combat(hard)
    clear()
    print("You reached the end.")
main()