from .factory import factory


class manager:
    def __init__(self):
        import pyautogui
        pyautogui.PAUSE = 0
        self.mouse = factory.get_mouse()
        self.keyboard = factory.get_keyboard()
    
    def execute(self, action):
        if action['type'] == 'move':
            self.mouse.move(action['x'], action['y'])
        elif action['type'] == 'click':
            self.mouse.click()
