from .vision import vision


def run_vision(frame_queue):
    with vision(frame_queue) as app:
        app.run()
