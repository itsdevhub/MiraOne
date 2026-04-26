import httpx
import websockets


HOST = '127.0.0.1'
PORT = 8000
API_URL = f'http://{HOST}:{PORT}'
API_WS = f'ws://{HOST}:{PORT}'

async def start_controller():
    async with httpx.AsyncClient() as client:
        res = await client.post(f'{API_URL}/controller/start')
        return res.json()

async def stop_controller():
    async with httpx.AsyncClient() as client:
        res = await client.post(f'{API_URL}/controller/stop')
        return res.json()

async def vision_stream():
    uri = f'{API_WS}/controller/vision/frame'

    async with websockets.connect(uri) as ws:
        while True:
            frame_bytes = await ws.recv()
            yield frame_bytes
