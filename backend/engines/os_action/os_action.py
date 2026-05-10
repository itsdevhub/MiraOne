import pyautogui

from queue import Empty as EmptyQueueException


class os_action:
    def __init__(self, actions_queue):
        pyautogui.PAUSE = 0
        self.actions_queue = actions_queue
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def run(self):
        while True:
            try:
                action = self.actions_queue.get_nowait()
                if action['type'] == 'move':
                    self.move_to(action['x'], action['y'])
                elif action['type'] == 'click':
                    self.click()
            except EmptyQueueException:
                pass
            except KeyError:
                pass
            except Exception:
                break

    def move_to(self, x, y):
        pyautogui.moveTo(x, y)

    def click(self):
        pyautogui.click()
