from .mouse import mouse
from .keyboard import keyboard


class factory:
    @staticmethod
    def get_mouse():
        return mouse()

    @staticmethod
    def get_keyboard():
        return keyboard()
