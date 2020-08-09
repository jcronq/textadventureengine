import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from pydantic import BaseModel
import uvicorn

import src.core.multi_game_manager as game_mgr

frontend = "xterm";
if os.path.exists(f"{frontend}_frontend"):
    public_dir = f"{frontend}_frontend/build"
else:
    public_dir = f"../{frontend}_frontend/build"

app = FastAPI()
app.mount("/static",StaticFiles(directory=f"{public_dir}/static"),'static')

class StartRequest(BaseModel):
    user: str
    game: str
    password: str

class UpdateRequest(BaseModel):
    session_id: str
    command: str

@app.get("/api/.*", status_code=404)
def invalid_api():
    return None

@app.post("/game/start")
def startGame(start_req: StartRequest):
    return game_mgr.startGame(start_req.user, start_req.password, start_req.game)

@app.post("/game/update")
def updateGame(update_req: UpdateRequest):
    return game_mgr.updateGame(update_req.session_id, update_req.command)

@app.get("/game/list")
def getGames():
    games = game_mgr.listGames()
    return {"status":"success", 'games': games}

@app.get("/health")
def healthCheck():
    return {"status": "not implemented"}

@app.get("/", include_in_schema=False)
def root():
    return FileResponse(f'{public_dir}/index.html')

@app.get("/manifest.json", include_in_schema=False)
def root():
    return FileResponse(f'{public_dir}/manifest.json')

@app.get("/logo192.png", include_in_schema=False)
def root():
    return FileResponse(f'{public_dir}/logo192.png')

if __name__ == "__main__":
    print("Starting up application")
    uvicorn.run("server:app", host="0.0.0.0", port=8000, log_level="debug")

