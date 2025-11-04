from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from .main_logic import collect_stats
from .utils import load_config
import os

app = FastAPI(title="GitLab Code Stats API")

class StatsRequest(BaseModel):
    start_date: str = None
    end_date: str = None
    users: list = None

@app.post("/code-stats")
def stats(request: StatsRequest):
    config_path = "config.json"
    collect_stats(
        start_date=request.start_date,
        end_date=request.end_date,
        users=request.users,
        config_path=config_path
    )
    config = load_config(config_path)
    output_file = os.path.join(os.getcwd(), config["output_filename"])
    if os.path.exists(output_file):
        return FileResponse(output_file, filename=config["output_filename"])
    return JSONResponse({"success": False, "message": "No data generated"})

def start_web():
    import uvicorn
    config = load_config("config.json")
    uvicorn.run(app, host="0.0.0.0", port=config["port"])
