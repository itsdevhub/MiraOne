from .fast_api_app import fast_api_app


def run_controller():
    with fast_api_app() as app:
        app.run()
