from fastapi import FastAPI
import uvicorn

from .controller import controller
from .controller_routes import controller_routes


class fast_api_app:
    HOST = '127.0.0.1'
    PORT = 8000

    def __init__(self):
        self.app = FastAPI()
        self.controller = controller(self)
        self.routes = controller_routes(self.controller)
        self.app.include_router(self.routes.router)
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def run(self):
        self.controller.start()

        config = uvicorn.Config(self.app, host=self.HOST, port=self.PORT, log_level='info')
        self.server = uvicorn.Server(config)
        self.server.run()
    
    def shutdown(self):
        self.controller.shutdown()
        self.server.should_exit = True

        return True
