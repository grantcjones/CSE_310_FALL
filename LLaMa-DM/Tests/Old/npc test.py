import ollama
import json
import os

def clear():
    print("\033[H\033[J")

npc_context = {}

# The prompt engineering needs work, as there's still some hallucinations.
# Notably, an NPC mentioned "dark fantasy", which is in its system prompt.
# Breaking the forth wall is obviously pretty bad.

with open(f'npc_context.json') as context_file:
    try:
        npc_context = json.load(context_file)
    except:
        ""

def dialog(name, prompt):
    clear()
    finish = ''
    context = []
    try:
        context = npc_context[f'{name}']
    except:
        npc_context[f'{name}'] = []
    stream = ollama.generate(
        model=f'{name}',
        prompt=prompt,
        stream=True,
        context=context
    )
    for chunk in stream:
        if not "EXIT" in chunk['response']:
            finish += chunk['response']
            print(chunk['response'], end='', flush=True)
            try:
                context = chunk['context']
            except:
                "" 
        else:
            npc_context[f'{name}'] = context
            with open('npc_context.json', 'w') as f:
                json.dump(npc_context, f)
            return chunk['response'].strip('_')
    npc_context[f'{name}'] = context
    with open('npc_context.json', 'w') as f:
        json.dump(npc_context, f)
    print("\n")
    return False
    

def talk_to_npc(name):
    exit = False
    while exit == False:
        user_input = input()
        clear()
        exit = dialog(name, user_input)
    ollama.generate(f'{name}', '', keep_alive=0)

    print(f"\nEnd communication: {exit}")


talk_to_npc('Edward')