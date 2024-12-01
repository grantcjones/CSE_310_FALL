#--------------------------------------------------------------------------------------------------------------
#   Dependancies
#--------------------------------------------------------------------------------------------------------------

import threading
from Modules.simplify import wait
from Modules.simplify import clear
from Modules.simplify import show_cursor
from Modules.simplify import hide_cursor

#--------------------------------------------------------------------------------------------------------------
#   Class
#--------------------------------------------------------------------------------------------------------------

class LoadingScreen:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoadingScreen, cls).__new__(cls)
        return cls._instance

    def __init__(self):
    #  Load stopped means that the load function has announced it's finished.
    #  Stop loading tells the load function to stop.
        self.load_stopped = threading.Event()
        self.stop_loading = threading.Event()
    
    def load(self, reason='loading'):
        "Only used internally, use the start method to start a loading screen."
        hide_cursor()
        clear()
        animation = ["\\", "|", "/", "-"]
        index = 0
        while not self.stop_loading.is_set():
            clear()
            print(f"{reason.title()}... {animation[index]}")
            index = (index + 1) % len(animation)
            wait(0.1)
        self.load_stopped.set()
        show_cursor()
        clear()
    
    def stop(self):
        
    #  Tell the load function to stop, and wait for it to say it's done stopping.
        "Stops the current loading screen."
        self.stop_loading.set()
        self.load_stopped.wait()

    def start(self, reason='loading'):
    #  Set up load_stopped and stop_loading.
        "Begins a loading screen in the console. Optionally displays the reason for loading."
        self.load_stopped.clear()
        self.stop_loading.clear()
        threading.Thread(target=self.load, args=(reason,)).start()