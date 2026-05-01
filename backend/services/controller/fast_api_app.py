from fastapi import FastAPI

from .controller import controller
from .controller_routes import controller_routes


class fast_api_app:
    def __init__(self):
        self.app = FastAPI()
        self.controller = controller()
        self.routes = controller_routes(self.controller)
        self.app.include_router(self.routes.router)
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
