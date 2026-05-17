from .fastapi_app import fastapi_app


def run_controller():
    with fastapi_app() as app:
        app.run()
