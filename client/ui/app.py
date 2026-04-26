import sys
import asyncio
from qasync import QEventLoop
from PySide6.QtWidgets import QApplication

from .main_window import main_window


def run_ui():
    app = QApplication(sys.argv)
    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    window = main_window()
    window.resize(400, 200)
    window.show()

    with event_loop:
        event_loop.run_forever()
