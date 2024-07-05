import os
import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI()
json_file = os.path.join(os.path.dirname(__file__), 'graphics_cards.json')

def load_json():
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data

class CORSMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope['type'] == 'http':
            request = Request(scope)
            response = await self.app(request)
            response.headers['Access-Control-Allow-Origin'] = '*'  # Replace with specific origin in production
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = '*'
            return response
        else:
            await self.app(scope, receive, send)

@app.get("/gpu-data")
async def get_gpu_data():
    try:
        data = load_json()
        return data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="JSON file not found")

@app.get("/")
async def get_index():
    return FileResponse('index.html')

if __name__ == "__main__":
    app.add_middleware(CORSMiddleware)
    uvicorn.run(app, host="127.0.0.1", port=8000)
