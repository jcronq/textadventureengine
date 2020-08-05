import os
import yaml

from src.core.parser import Parser
from src.core.engine import Engine
from src.config.load import GameLoader
from src.text.views import htmlPrint

import src.text.textUtils as txtUtil
import uuid

data_dir = os.environ.get("GAME_DATA_DIR", f'{os.environ["HOME"]}/.data')

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

users_dir = f"{data_dir}/users"

try:
    users = os.listdir(users_dir)
except:
    os.makedirs(users_dir)
    users = []

running_games = {}
session_map = {}
password_map = {}
available_games = os.listdir('./games')

for user in users:
    try:
        with open(f"{users_dir}/{user}/meta.yaml", 'r') as f:
            user_meta = yaml.full_load(f.read())
            session_id = user_meta['meta']['session_id']
            password_hash = user_meta['meta']['pass']
            session_map[user] = session_id
            password_map[user] = password_hash
    except:
        pass

def listGames():
    return available_games

def startGame(user_id, password, game_name):
    if game_name not in available_games:
        return {
            "success": False,
            "session_id": None,
            "text": f"Uknown Game: {game_name}"
        }
    if user_id in session_map:
        return {
            "success": False,
            "session_id": None,
            "text": f"Username already in use."
        }
    else:
        session_id = uuid.uuid4()

    session_map[user_id] = str(session_id)
    password_map[user_id] = password

    user_dir = f"{users_dir}/{user_id}"

    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    with open(f"{user_dir}/meta.yaml", 'w') as f:
        f.write(yaml.dump(
            {
                'meta': {
                    'session_id': str(session_id),
                    'pass': password
                }
            }
        ))

    gameLoader = GameLoader(game_name)
    game = gameLoader.getGameObject()
    parser = Parser()
    engine = Engine(game, parser)
    running_games[str(session_id)] = engine

    initial_game_text = engine.update(htmlPrint, 'examine', debug=False)

    return {
        "success": True,
        "session_id": str(session_id),
        "text": [f"Welcome to {txtUtil.properNoun(game_name)}!"] + initial_game_text
    }

def updateGame(session_id, cmd):
    print(session_id, running_games.keys())
    if session_id not in running_games:
        return {
            "success": False,
            "session_id": session_id,
            "text": [f"Game not found for {session_id}.  Call load, or start."]
        }

    game_engine = running_games[session_id]
    game_text = game_engine.update(htmlPrint, cmd, debug=False)

    return {
        "success": True,
        "session_id": session_id,
        "text": game_text
    }

