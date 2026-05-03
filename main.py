from multiprocessing import Process

from backend.services.controller import run_controller
from client.ui import run_ui
from client.api import shutdown_controller


if __name__ == '__main__':
    controller_process = Process(target=run_controller)
    controller_process.start()

    try:
        run_ui()
    finally:
        shutdown_controller()
        controller_process.join()
