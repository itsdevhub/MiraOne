from .vision import vision


def run_vision(frame_queue, actions_queue):
    with vision(frame_queue, actions_queue) as app:
        app.run()
