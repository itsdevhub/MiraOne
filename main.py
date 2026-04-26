from multiprocessing import Process

from backend.services.controller import run_controller
from client.ui import run_ui


if __name__ == '__main__':
    controller_process = Process(target=run_controller)
    controller_process.start()

    try:
        run_ui()
    finally:
        controller_process.terminate()
        controller_process.join()
