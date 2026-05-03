from .engine_manager import engine_manager


class controller:
    def __init__(self, fast_api_app):
        self.fast_api_app = fast_api_app
        self.engine_manager = engine_manager()

    def start(self):
        return self.engine_manager.start()

    def stop(self):
        return self.engine_manager.stop()

    def get_frame_queue(self):
        return self.engine_manager.vision_engine.frame_queue
