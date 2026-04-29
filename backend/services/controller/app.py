from fastapi import FastAPI, WebSocket
import uvicorn

from .engine_manager import engine_manager


app = FastAPI()
engine_manager = engine_manager()

@app.post('/controller/start')
def start_controller():
    return engine_manager.start()

@app.post('/controller/stop')
def stop_controller():
    return engine_manager.stop()

@app.websocket('/controller/vision/frame')
async def vision_stream(websocket: WebSocket):
    vision_frame_queue = engine_manager.vision_engine.frame_queue
    await websocket.accept()

    while True:
        if not vision_frame_queue.empty():
            vision_frame = vision_frame_queue.get()
            await websocket.send_bytes(vision_frame)

def run_controller():
    uvicorn.run(app, host='127.0.0.1', port=8000)
