import random
import json
from Modules.simplify import clear, wait

AI_INTENT = True
if AI_INTENT == True:
    from Modules.ai import AI
    ai = AI()

#
#           Root ---v                           # The root is the entire decision tree
#                   Tree ---v                   # The tree is the current decision
#                        Branches               # Branches are any branching decisions from the current one.
#                                               # The distinction between the branch (singular) and branches (plural) is that
#                                               # branch is used by the interpreter to refer to the new tree during switching.

# Format:
# 'tree':{                                      # The name of the new set of choices.          *Not optional. 
#     'statement':'description',                # The opening statement.                       *Not optional. 
#     'question':'question',                    # Optional. The question for the player.
#     'do':['function name', [varaible(s)]]     # Heavily optional and experimental. Executes functions from the main python file.
#     'options':{                               # Optional. The code will detect it's a dead end and go back.
#           'odds':[50, 50],                    # Optional. This overrides player choice and leaves the options to specified chances.
#           'branch':{},                        # List of the next set. It's a choice by default if odds isn't present
#           'other branch':{}                   # You can have as many branches as you want. If odds is used, EACH branch must have one.
#
#     }
#     'repeat'=True                             # Optional. Goes back to the beginning of the root.
#     'exit'=True                               # Optional. Exits the interpreter.
# }

# To use a decision tree made by scratch, you have to pass it into interpret() as the argument. Keep in mind, you must have either a question or odds at the root of the tree. After that, you won't need to. You can have just a statement for descriptions and such.
# root = {
#     'options':{
#         'odds':[100],
#         'main':{
#             'statement':'description',
#             'question':'question',
#             'options':{
#                 'odds':[100],
#                 'branch':{},
#             }
#         }
#     }
# }

root = {
    'options':{
        'odds':[50, 50],
        'door':{
            'statement':'You approach a door.',
            'question':'Would you like to enter?',
            'options':{
                'description':{
                    'statement':'The door is inlaid in a mountain face. It is made of wood and has a golden doorknob. Though covered in dust and cobwebs, they seem to be in pristine condition.'
                },
                'enter':{
                    'statement':'You see a dark hallway.',
                    'question':'Proceed?',
                    'options':{
                        'proceed':{
                            'do':[['test', ['preston', 'jacob']]],
                            'options':{
                                'odds':[20, 80],
                                'dead':{
                                    'statement':'You have died.',
                                    'repeat':True
                                },
                                'live':{
                                    'statement':'You survived.',
                                    'repeat':True
                                }
                            },
                        },
                        'turn back':{
                            'statement':'You turned back.',
                            'repeat':True
                        }
                        
                    }
                }
            }
        },
        'village':{
            'statement':'You approach a village.',
            'question':'Would you like to proceed?',
            'options':{
                'proceed':{
                    'options':{
                        'odds':[50,50],
                        'talk':{
                            'statement':'You see Edward and Elise',
                            'question':'Who would you like to speak to?',
                            'options':{
                                'elise':{
                                    'statement':'You spoke to Elise',
                                    'repeat':True
                                },
                                'edward':{
                                    'statement':'You spoke to Edward',
                                    'repeat':True
                                }
                            }
                        },
                        'trip':{
                            'statement':'You tripped and fell.'
                        }
                    }
                }
            }
        }
    }
}

#             Read
# with open('decision trees/tree.root') as file:
#     root = json.load(file)

#            Write
# with open('tree.root', 'w') as file:
#     json.dump(root, file, indent=4)

# Tree accessable functions
def test(name, other_name):
    print("hello", name, "from", other_name)

functions = {
    "test": test,
}

# Tree accessable function execution
def do(func_name:str, variables:list=[]):
    "Calls a function from the 'functions' dictionary."
    return functions[func_name](*variables)

def check_do(tree:dict):
    "Parses the tree for functions to call."
    if 'do' in list(tree):
        functions = tree['do']
        for func_name, variables in functions:
            do(func_name, variables)

# The parser for the interpreter
def parse(tree:dict, previous:dict, root:dict) -> dict:
    "Outputs either a player chosen or randomly chosen new tree."
    # Look to see if options exist, if not it treats it as just a message to the player.
    check_do(tree)
    if 'options' in list(tree):
        options = tree['options']

        # Checks to see if there's any odds added in. Odds override choice.
        if 'odds' not in list(options):
            found = None
            while found == None:
                statement = tree['statement']
                option_list = ', '.join(options).title()

                print(statement)
                print(option_list)

                # Retrieve question or use the default
                if 'question' in list(tree):
                    question = tree['question']
                else:
                    question = 'What would you like to do?'

                # Ask the player the question.
                if AI_INTENT == True:
                    user_input = ai.intent(input(question + ' '), f"{tree['statement']} {question}", list(options)).strip(', .').lower()
                else:
                    user_input = input(question + ' ').strip(', .').lower()

                # Check for a match.
                if user_input in list(options):
                    print('[MATCH]')
                    found = options[user_input]
                    return found
        # Plays the odds.
        else:
            odds = options['odds']
            for option, odd in enumerate(odds):
                pick = list(options.keys())[option + 1]
                if option != len(odds)-1:
                    chance = random.random() * 100
                    if odd <= chance:
                        check_do(tree)
                        tree = options[pick]
                        return tree
                else:
                    check_do(tree)
                    tree = options[pick]
                    return tree
    else:
        # Prints a message.
        if 'statement' in list(tree):
            input(tree['statement'])
            if 'repeat' in list(tree):
                # Goes back to the beginning of the decision tree.
                check_do(tree)
                return root
            if 'exit' in list(tree):
                check_do(tree)
                return 'exit'
        check_do(tree)
        return previous

# The interpreter
def interpret(root:dict) -> None:
    "Starts a parsing loop for a tree."
    tree = root
    previous = root
    while True:
        clear()
        branch = parse(tree, previous, root)
        if branch != 'exit':
            previous = tree
            tree = branch
        else:
            break
    print("END OF")
        
def main():
    interpret(root)

main()