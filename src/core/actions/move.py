import src.text.textIO as txt
from src.core.actions.examine import examine
from src.core.actions.help import actionHelp
from src.core.stateManager import StateManager

def move(game, args={}):
    if len(args) == 0:
        moveHelp()
    else:
        new_location_name = args.get('location', None)
        if new_location_name is None or new_location_name == '':
            txt.printGameBlock("I don't understand where you want me to go.")
            return
        current_location = game.getPlayerLocation()
        current_location_name = current_location.name
        location_print = getLocationPrint(new_location_name)

        travel_txt = []
        blockade_result = blockadeClear(game, current_location, new_location_name)
        if blockade_result['block_cleared']:
            # import pdb; pdb.set_trace()
            travel_description = current_location.travel_descriptions.get(
                new_location_name.lower(),
                None
                )
            if blockade_result.get('txt', None) is not None:
                travel_txt.append(blockade_result['txt'])
            if travel_description is not None:
                travel_txt.append(travel_description)
            if new_location_name in current_location.connections.keys():
                new_location_state = f'location.{new_location_name}'
                new_location_visited = f'{new_location_state}.visited'
                first_visit = game.getState(new_location_visited, default=False)
                game.setState(new_location_visited, True)

                game.setPlayerLocation(new_location_name)
                travel_txt += getLocationTextBlock(game)
            else:
                travel_txt.append(f"I can't find a way {location_print}")
        else:
            if blockade_result.get('txt', None) is not None:
                travel_txt.append(blockade_result.get('txt'))
            else:
                travel_txt.append(f"I don't seem to be able to go {location_print} yet...")

            travel_txt += getLocationTextBlock(game)

        txt.printGameBlock(travel_txt)

def getLocationPrint(new_location_name):
    if new_location_name in ['north', 'south', 'east', 'west']:
        return f"to the {new_location_name}"
    elif new_location_name in ['up', 'down']:
        return f"{new_location_name}"
    else:
        return f"to {new_location_name}"

def getLocationTextBlock(game):
    location_txt = []
    new_location = game.getPlayerLocation()
    location_txt.append(new_location.examine())
    items = game.getItemsInLocation(new_location.name)
    if len(items) == 0:
        item_description = ["Nothing noteworthy here."]
    else:
        item_description = ["*Items:*"]+list(['- '+item.describe() for item in items])
    location_txt += ["<br>".join(item_description)]
    return location_txt

def blockadeClear(game, current_location, new_location_name):
    blocker = current_location.blockades.get(new_location_name, None)
    if blocker is None:
        return {
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
        'block_cleared': block_cleared,
        'txt': success if block_cleared else failure,
    }

def moveHelp():
    actionHelp("move", "Use move to get to different places.\n ex)move up")

