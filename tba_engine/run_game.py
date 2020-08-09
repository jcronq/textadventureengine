import os

# from functools import filter

from src.text.textIO import getOption, utilPrint
from src.core.game import Game
from src.core.parser import Parser
from src.core.engine import Engine
from src.config.load import GameLoader
from src.text.views import htmlPrint, bashPrint, bashBlockPrint, bashRawPrint

data_dir = f"{os.environ['HOME']}/.data"
save_dir = f"{data_dir}/save"

available_games = os.listdir('./games')

if len(available_games) > 1:
    prompt = "Which game would you like to play?"
    options = available_games
    choice = getOption(prompt, options, 0)
    game_name = options[choice]
else:
    game_name = available_games[0]

utilPrint(f"Welcome to {game_name}!")
gameLoader = GameLoader(game_name)
game = gameLoader.getGameObject()

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

save_files = os.listdir(save_dir)
if len(save_files) > 0:
    options = filter(lambda n: n.contains(game_name), save_files)
    options.append("New Game")
    new_game_opt = len(save_files)-1
    choice = -1
    while choice != -1:
        choice = getOption(
            "Load Saved Game?",
            options,
            default_selection = new_game_opt
        )
        if choice != new_game_opt:
            try:
                with open(options[choice], 'r') as f:
                    game_state = json.loads(f.read())
            except:
                print("ERROR: Failed to load file {options[choice]}")
                choice = -1
        else:
            player_name = input('name? > ')
            game_state ={
                'player': {
                    'name': player_name,
                }
            }

    game.load(game_state)

parser = Parser()
engine = Engine(game, parser)
engine.run_loop(bashPrint, debug=False)

