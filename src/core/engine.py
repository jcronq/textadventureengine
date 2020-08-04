import src.text.textIO as txt

from src.core.actions.move import move
from src.core.actions.take import take
from src.core.actions.examine import examine
from src.core.actions.inventory import inventory
from src.core.actions.drop import drop

GAME_RUNNING = True

def quitGame(game, args):
    global GAME_RUNNING
    GAME_RUNNING = False

def printCommand(game, args):
    target = args.get('target', None)
    if target is None or target == 'state':
        print(game.stateManager.state)

command_handlers = {
    "move": move,
    "take": take,
    "examine": examine,
    "inventory": inventory,
    "drop": drop,
    "print": printCommand,
    "quit": quitGame,

}

class Engine:
    def __init__(self, game, parser):
        self.game   = game
        self.parser = parser

    def run(self, debug=False):
        command = command_handlers.get('examine', None)
        command(self.game, {})
        while GAME_RUNNING:
            in_str = txt.getInput()
            command_obj = self.parser.parse_command(in_str)
            if debug:
                txt.utilPrint(f"State: {self.game.getFullState()}")
            command = command_handlers.get(command_obj['intent'], None)
            if command is not None:
                if debug:
                    txt.utilPrint(f"Calling: {command_obj['intent']}(game, {command_obj['args']})")
                command(self.game, command_obj['args'])
            else:
                txt.utilPrint(f"Unknown command: {command_obj['intent']}")
        txt.utilPrint(f"Exiting game.")

