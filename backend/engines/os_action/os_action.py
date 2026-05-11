from queue import Empty as EmptyQueueException

from .driver.manager import manager


class os_action:
    def __init__(self, actions_queue):
        self.actions_queue = actions_queue
        self.driver_manager = manager()
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def run(self):
        # TODO: replace with condition
        while True:
            try:
                action = self.actions_queue.get_nowait()
                self.driver_manager.execute(action)
            except EmptyQueueException:
                pass
            except KeyError:
                pass
            except Exception:
                break
