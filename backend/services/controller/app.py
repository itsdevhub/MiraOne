from fastapi import FastAPI, WebSocket
import uvicorn
import asyncio

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
        try:
            vision_frame = vision_frame_queue.get_nowait()
            await websocket.send_bytes(vision_frame)
        except Exception:
            await asyncio.sleep(0.01)

def run_controller():
    uvicorn.run(app, host='127.0.0.1', port=8000)
