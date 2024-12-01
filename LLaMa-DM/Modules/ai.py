#--------------------------------------------------------------------------------------------------------------
#   Dependancies
#--------------------------------------------------------------------------------------------------------------

from Modules.loading import LoadingScreen
import ollama
import time

from Modules.simplify import wait

#--------------------------------------------------------------------------------------------------------------
#   Initialization
#--------------------------------------------------------------------------------------------------------------

loading = LoadingScreen()

#--------------------------------------------------------------------------------------------------------------
#   Class
#--------------------------------------------------------------------------------------------------------------

# Used for formatting. It's the exact length of the editing window in 1080p.
BLOCK = '----------------------------------------------------------------------------------------------------------------------------------------'
# Used for formatting. It's the exact length of the editing window in 1080p.
BLOCK = '----------------------------------------------------------------------------------------------------------------------------------------'

class AI():
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AI, cls).__new__(cls)
        return cls._instance

    def __init__(self):
    #  Settings
        self.refresh = 3                          # Max retries for the vote system.
        self.votes = 3                            # Number of votes for the vote system.
        self.basic_choices = ['check inventory']  # The default options for the player.
        self.version = 'llama3.2:latest'          # The LLM used for the program.
        self.situation_context = []               # Used for saving AI context.

    #  Statistics
        self.total_time = 0
        self.refreshes = 0
        self.tries = 0

    with open('data/log.txt', 'w') as file: 
        file.write(BLOCK)
    
    # Ask a question and get the intent
    def ask(self, query:str, options:list, setting:str=None, show_basic_options=True, testing=False) -> str:
        '''
        Asks the player a given question and matches the intent to a set of options.
        Optionally, it'll rephrase the current setting.
        You can also choose whether or not to show the basic options, like checking inventory.
        '''
        # If a setting was given, create a prompt for merging it with the question. Otherwise, just rephrase the question.
        if setting:
            loading.start('Generating setting')
            setting = self.redescribe(setting)
            loading.stop()
            question = f'You\'re a detached narrator. Take this setting description: "{setting}" and this question :"{query}" and simplify them into a short question. Don\'t put it in quotes.'
        else:
            question = f'You\'re a detached narrator. Rephrase "{query}" in a simple, direct question. Don\'t put it in quotes or explain yourself.'

        # Generate question 
        loading.start('Generating question')
        rephrased_question = ollama.generate(self.version, question)['response']
        loading.stop()

        # Display in this order: Setting, question, options, input space.
        print('---------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        if setting:
            print(setting)
            print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
        print(rephrased_question)
        # print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
        # # Create the options string for the player and print it
        # basic_options = ['check inventory']
        # option_string = f", ".join(list(options)) + ', ' + f", ".join(list(self.basic_choices)) if show_basic_options else ", ".join(options)
        # print(f'Options: {option_string.title()}')
        print('---------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        
        # Actually ask the question. Testing mode just uses AI to answer itself for debug purposes.
        if testing == False:
            # Ask the question and return the intent
            question = input()
            return self.intent(question, query, options, setting)
        else:
            loading.start('Generating answer')
            answer = self.answer(rephrased_question)
            loading.stop()
            return self.intent(answer, query, options, setting)
    
    # The AI will answer a question
    def answer(self, question:str, setting:str=None) -> str:
        "Generates the answer to a question. Designed for automating the ask method."
        prompt = f'Create a simple answer for the following as if you were a user: {question}'
        output = ollama.generate(self.version, prompt)['response']
        return output
    
    # TODO: Combine describe turn and describe action into a single function for clarity
    # Have the AI describe a combat turn
    def describe_turn(self, text:str) -> str:
        'Redescribes a situation based on input.'
        prompt = (
    f"Describe this combat turn in an engaging and illustrative way, "
    f"using the provided details exactly as written: \"{text}\". "
    f"Focus on vivid, concise imagery and avoid adding any objects or details not provided. "
    f"Ensure the description flows naturally without quotation marks or explanations."
    f"Only describe the attack and the damage number."
    f"Use 60 words or less.")
        output = ollama.generate(self.version, prompt)['response']
        return output
    
    def describe_action(self, text:str) -> str:
        'Redescribes a situation based on input.'
        prompt = f'Rephrase the following action update in a short sentence: "{text}". It shouldn\'t be in quotes or come with an explanation.'
        output = ollama.generate(self.version, prompt)['response']
        return output
    
    # TODO: Change "redescribe" to "describe_setting" in all files, this one included.
    # Have the AI rephrase something in a dark, poetic way
    def redescribe(self, text:str) -> str:
        'Redescribes a setting.'
        prompt = f'Rephrase the following dark fantasy style in a short paragraph: {text}. Don\'t make it unclear what the original text was.'
        output = ollama.generate(self.version, prompt)['response']
        return output
        
    
    # Extract intent
    def intent(self, text:str, query:str, options:list, setting:str=None, basic_options=False) -> str:
        refresh = 0
        start = time.time()
        while refresh < self.refresh:
            refresh += 1
            self.refreshes += 1
            self.tries += 1
            loading.start('Processing')
        
            # Assemble the options string
            if basic_options != False:
                options += self.basic_choices
            option_string = f", ".join(list(options)) + f", ".join(list(basic_options)) if basic_options else ", ".join(options)

            # Start grabbing intent votes
            prompt = f'Get user intention from the following text: "{text}" from the following context: "{setting + query if setting else query}" out of the following options: "{option_string}". Your output must STRICTLY be from the list of options. After that, explain your reasoning in one short sentence. Ignore hesitation.'
            compilation = ''
            for i in range(self.votes):
                compilation += f'{ollama.generate(self.version, prompt)['response']}\n'
                compilation += f'{ollama.generate(self.version, prompt)['response']}\n'
            loading.stop()

            # Tally the vote
            loading.start('Analyzing')
            prompt = f"Look at the following and ONLY output the most commonly picked choice, NOT any kind of reasoning, punctuation, or list: [\n{compilation}]."
            outcome = ollama.generate(self.version, prompt)['response']

            # Stop loading and return the outcome of the vote
            loading.stop()
            if outcome.lower().strip(', ."') in options:
                stop = time.time()
                elapsed = stop-start
                self.total_time += elapsed
                with open('data/tracker.txt', 'w') as file:
                        average = self.total_time/self.tries
                        debug = f'Question: {query}\nOptions: {', '.join(options)}\nAnswer: {text}\nResult: {outcome}\nAverage: {average:.2f}\nAttempts:{self.refreshes}\nTotal Tries:{self.tries}'
                        debug = f'Question: {query}\nOptions: {', '.join(options)}\nAnswer: {text}\nResult: {outcome}\nAverage: {average:.2f}\nAttempts:{self.refreshes}\nTotal Tries:{self.tries}'
                        file.write(debug)
                with open('data/log.txt', 'a') as file: 
                    log = f'\nQuestion: {query}\nAnswer: {text}\nResult: {outcome}\nReasoning: [\n{compilation}]\nElapsed: {elapsed}\nAttempts:{refresh}/3\n{BLOCK}'
                    log = f'\nQuestion: {query}\nAnswer: {text}\nResult: {outcome}\nReasoning: [\n{compilation}]\nElapsed: {elapsed}\nAttempts:{refresh}/3\n{BLOCK}'
                    file.write(log)
                return outcome.lower().strip(', ."')
            print(f'{refresh}/{self.refresh}')
        print("Intent not found.")


            