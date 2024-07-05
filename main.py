import os
import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse, PlainTextResponse
import uvicorn

app = FastAPI()
json_file = os.path.join(os.path.dirname(__file__), 'graphics_cards.json')

def load_json():
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data

ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    origin = request.headers.get('origin')
    if request.method == "OPTIONS":
        response = PlainTextResponse()
        if origin in ALLOWED_ORIGINS:
            response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = '*'
        return response
    response = await call_next(request)
    if origin in ALLOWED_ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response

@app.get("/gpu-data")
async def get_gpu_data():
    try:
        data = load_json()
        return JSONResponse(content=data)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="JSON file not found")

@app.get("/")
async def get_index():
    return FileResponse('index.html')

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

