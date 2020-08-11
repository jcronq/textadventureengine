import src.text.textIO as txt

from src.actions.move import move
from src.actions.take import take
from src.actions.examine import examine
from src.actions.inventory import inventory
from src.actions.drop import drop

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
    "talk": talk,
    "print": printCommand,
    "quit": quitGame,
}

class Engine:
    def __init__(self, game, parser):
        self.game   = game
        self.parser = parser

    def update(self, game_printer, in_str, debug=False):
        if self.game.inConversation():
            command_obj = {
                'intent': 'talk',
                'args': {
                    'character': self.game.getConversingNPC(),
                    'selection': self.parser.parseConvoInput(in_str),
                }
            }
        else:
            command_obj = self.parser.parse_command(in_str)
        if debug:
            txt.utilPrint(f"State: {self.game.getFullState()}")
        command = command_handlers.get(command_obj['intent'], None)
        if command is not None:
            if debug:
                txt.utilPrint(f"Calling: {command_obj['intent']}(game, {command_obj['args']})")
            command(self.game, command_obj['args'])
            return game_printer(self.game.getText())
        else:
            return [f"Unknown command: {command_obj['intent']}"]


    def run_loop(self, game_printer, debug=False):
        command = command_handlers.get('examine', None)
        command(self.game, {})
        game_printer(self.game.getText())
        while GAME_RUNNING:
            in_str = txt.getInput()
            self.update(game_printer, in_str, debug)
        txt.utilPrint(f"Exiting game.")

