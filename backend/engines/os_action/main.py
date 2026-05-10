from .os_action import os_action


def run_os_action(actions_queue):
    with os_action(actions_queue) as app:
        app.run()
