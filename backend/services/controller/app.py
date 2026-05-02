import uvicorn

from .fast_api_app import fast_api_app


def run_controller():
    with fast_api_app() as app:
        app.controller.start()
        uvicorn.run(app.app, host="127.0.0.1", port=8000)
