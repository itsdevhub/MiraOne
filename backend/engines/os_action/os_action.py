import time
import pyautogui

from queue import Empty as EmptyQueueException


class os_action:
    def __init__(self, actions_queue):
        self.actions_queue = actions_queue
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def run(self):
        while True:
            try:
                action = self.actions_queue.get_nowait()
                print(str(action))
            except EmptyQueueException:
                time.sleep(0.01)
