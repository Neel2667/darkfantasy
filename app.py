from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import json
import threading
from main import PsychoStudioEngine

app = FastAPI()

# Global state to track progress and logs
state = {
    "status": "Idle",
    "logs": [],
    "video_ready": False,
    "video_path": ""
}

class WebLogger:
    def info(self, message):
        print(f"[INFO] {message}")
        state["logs"].append(message)
        state["status"] = message

def run_production(topic, length, groq_key, pexels_key):
    global state
    state["logs"] = []
    state["video_ready"] = False
    
    # 1. Update config
    config = {
        "api_keys": {
            "groq": groq_key,
            "pexels": pexels_key
        }
    }
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    # 2. Run Engine
    try:
        engine = PsychoStudioEngine(topic, length=int(length))
        engine.run_full_pipeline()
        
        video_path = "outputs/final/FINAL_VIDEO.mp4"
        if os.path.exists(video_path):
            state["video_ready"] = True
            state["video_path"] = "/video"
            state["status"] = "Production Complete!"
        else:
            state["status"] = "Error: Video missing."
    except Exception as e:
        state["status"] = f"Error: {str(e)}"

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("index.html", "r") as f:
        return f.read()

@app.post("/start")
async def start_task(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()
    background_tasks.add_task(
        run_production, 
        data['topic'], 
        data['length'], 
        data['groq_key'], 
        data['pexels_key']
    )
    return {"message": "Started"}

@app.get("/status")
async def get_status():
    return JSONResponse(state)

@app.get("/video")
async def get_video():
    from fastapi.responses import FileResponse
    return FileResponse("outputs/final/FINAL_VIDEO.mp4")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
