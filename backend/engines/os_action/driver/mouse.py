import pyautogui


class mouse:
    def move(self, x, y):
        pyautogui.moveTo(x, y)

    def click(self):
        pyautogui.click()
