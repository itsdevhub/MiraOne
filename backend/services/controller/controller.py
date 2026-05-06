import threading

from .engine_manager import engine_manager


class controller:
    def __init__(self, fast_api_app):
        self.fast_api_app = fast_api_app
        self.engine_manager = engine_manager()
        self.shutdown_event = threading.Event()

    def start(self):
        return self.engine_manager.start()

    def stop(self):
        return self.engine_manager.stop()

    def shutdown(self):
        self.stop()
        self.shutdown_event.set()
    
    def is_shutting_down(self):
        return self.shutdown_event.is_set()

    def get_frame_queue(self):
        return self.engine_manager.vision_engine.frame_queue
