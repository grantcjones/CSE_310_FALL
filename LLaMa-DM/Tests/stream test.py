import ollama

while True:
    context = []
    user_input = input()
    stream = ollama.generate('llama3.2:3b',prompt=user_input, stream=True)
    for chunk in stream:
        print(chunk['response'], end='', flush=True)
    