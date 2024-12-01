import sys
import threading
import os
import time
import random

loading_thread = 0

log = []

def loading_screen(reason="Loading"):
    animation = ["\\", "|", "/", "-"]
    index = 0

    this_thread = random.randint(1, 1000)

    global loading_thread
    loading_thread = this_thread

    while loading_thread == this_thread:
        start = time.time()
        os.system('cls')
        print(f"\r{reason}... {animation[index]}")
        index = (index + 1) % len(animation)
        stop = time.time()
        delay = start - stop
        log.append(delay)
        time.sleep(0.05)

loading_state = threading.Thread(target=loading_screen, args=('First loop',))
loading_state.start()
time.sleep(5)
loading_state.join()
print(":)")
time.sleep(3)

loading_state = threading.Thread(target=loading_screen, args=('Second loop',))
loading_state.start()

time.sleep(5)
loading_state.join()

# time.sleep(0.1)
# print(f"Average: {sum(log) / len(log)}")
# print(f"Greatest: {min(log)}")
# print(f"Lowest: {max(log)}")