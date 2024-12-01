import tkinter
import threading

class Menu:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Menu, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        menu = tkinter.Tk()
        menu.title = "AI DM"

        label = tkinter.Label(menu, text='AI DM')
        label.pack(padx=10, pady=10)

        situation = tkinter.Label(menu, text = "Situation", width=400, relief=tkinter.SOLID, borderwidth=1)
        situation.pack(padx=10, pady=5)

        response = tkinter.Label(menu, text = "Response", width=400, height=35, relief=tkinter.SOLID, borderwidth=1, anchor=tkinter.NW)
        response.pack(padx=10, pady=5)

        player_input = tkinter.Entry(menu, textvariable="Input", width=400, relief=tkinter.SOLID, borderwidth=1)
        player_input.pack(padx=10, pady=5)
        menu.mainloop()

        player_input.bind('<Return>', self.enter_text())
        self.situation = situation
        self.response = response
        self.player_input = player_input
        self.text_entered = threading.Event()

        self.player_input.bind('<Return>', self.reset_input_text)

    last_input = ''
    def reset_input_text(self):
        global last_input
        self.text_entered.set()
        last_input = self.player_input.get()
        

    def get_input(self):
        self.text_entered.wait()
        return last_input

    def change_situation(self, new_text):
        self.situation.config(text=new_text)

Menu()