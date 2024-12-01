import ollama
import json
import os

def clear():
    print("\033[H\033[J")

# The prompt engineering needs work, as there's still some hallucinations.
# Notably, an NPC mentioned "dark fantasy", which is in its system prompt.
# Breaking the forth wall is obviously pretty bad.

with open(f'situation_context.json') as context_file:
    try:
        context = json.load(context_file)
    except:
        context = []

with open(f'enemies.json') as context_file:
    try:
        enemies = json.load(context_file)
    except:
        enemies = []

def dialog(name, prompt):
    clear()
    global context
    stream = ollama.generate(
        model=f'{name}',
        prompt=prompt,
        stream=True,
        context=context
    )
    for chunk in stream:
        if not "EXIT" in chunk['response']:
            print(chunk['response'], end='', flush=True)
            try:
                context = chunk['context']
            except:
                ""
        else:
            return True
    print("\n")
    return False
    

def talk_to_npc(name):
    exit = False
    while exit == False:
        user_input = input()
        if user_input == "enemy list":
            user_input = str(enemies)
        clear()
        exit = dialog(name, user_input)

    ollama.generate(f'{name}', '', keep_alive=0)
    print("\nEnd communication.")


talk_to_npc('llama3.2:latest')