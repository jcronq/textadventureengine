from src.core.actions.examine import examine
from src.core.actions.help import actionHelp
from src.core.stateManager import StateManager
import src.text.messages as messageTxt
import src.text.describe as describe

def move(game, args={}):
    if len(args) == 0:
        moveHelp()
    else:
        path = args.get('location', None)
        # Missing location in request
        if path is None or path.strip() == '':
            game.report(messageTxt.malformed_move_request)
            return

        current_location = game.getPlayerLocation()
        current_location_name = current_location.name
        blockade_result = blockadeClear(game, current_location, path)

        travel_txt = []

        # No path
        if not current_location.hasPath(path):
            game.report(messageTxt.invalidPath(path))
            return

        # Path blocked
        if not blockade_result['block_cleared']:
            game.report(describe.blockedPath(path, blockade_result))
            examine()

        # Path not blocked
        else:
            # First time path unblocked
            if blockade_result['has_block']:
                previouslyCleared = game.getBlockerClearStatus(current_location.name, path)
                if not previouslyCleared:
                    game.report(describe.clearBlockade(blockade_result))
                    game.setBlockerClearStatus(current_location, path)

            game.report(describe.move(current_location, path))

            game.setPlayerLocation(path)
            examine(game, {})

def blockadeClear(game, current_location, new_location_name):
    blocker = current_location.blockades.get(new_location_name, None)
    if blocker is None:
        return {
            'has_block': False,
            'block_cleared': True,
            'txt': None,
        }
    failure = blocker.get('failure', None)
    success = blocker.get('success', None)
    value = blocker.get('value', None)
    state = blocker.get('state', None)
    block_cleared = False
    if state is not None:
        state_value = game.getState(state, default = None)
        block_cleared = state_value == value
    return {
        'has_block': True,
        'block_cleared': block_cleared,
        'txt': success if block_cleared else failure,
    }

def moveHelp():
    actionHelp("move", "Use move to get to different places.\n ex)move up")

