import asyncio
from fastapi import APIRouter, WebSocket


class controller_routes:
    def __init__(self, controller):
        self.controller = controller
        self.router = APIRouter()
        self._register_routes()

    def _register_routes(self):

        @self.router.post("/controller/start")
        def start_controller():
            return self.controller.start()

        @self.router.post("/controller/stop")
        def stop_controller():
            return self.controller.stop()

        @self.router.post("/controller/shutdown")
        def shutdown_controller():
            return self.controller.fast_api_app.shutdown()

        @self.router.websocket("/controller/vision/frame")
        async def vision_stream(websocket: WebSocket):
            await websocket.accept()
            vision_frame_queue = self.controller.get_frame_queue()

            while True:
                try:
                    vision_frame = vision_frame_queue.get_nowait()
                    await websocket.send_bytes(vision_frame)
                except Exception:
                    await asyncio.sleep(0.01)
