from multiprocessing import Process, Queue

from backend.engines.vision import run_vision


class base_engine:
    def __init__(self, target, args = ()):
        self.process = None
        self.target = target
        self.args = args

    def start(self):
        if self.is_running():
            return False

        self.process = Process(target=self.target, args=self.args)
        self.process.start()
        return True

    def stop(self):
        if not self.process:
            return False

        self.process.terminate()
        self.process.join()
        self.process = None
        return True
    
    def is_running(self):
        return self.process and self.process.is_alive()

class vision_engine(base_engine):
    def __init__(self):
        self.frame_queue = Queue(maxsize=10)
        super().__init__(target=run_vision, args=(self.frame_queue,))

# class os_action_engine(base_engine):
    # def __init__(self):
        # super().__init(target=run_os_action)

class engine_manager:
    def __init__(self):
        self.vision_engine = vision_engine()
        # self.os_action_engine = os_action_engine()
    
    def start(self):
        return self.vision_engine.start()
        # self.os_action_engine.start()
    
    def stop(self):
        return self.vision_engine.stop()
        # self.os_action_engine.stop()
