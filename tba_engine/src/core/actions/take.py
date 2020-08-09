from src.core.actions.help import actionHelp
import src.text.messages as messageTxt
import src.text.describe as describe

def take(game, args={}):
    container_name = args.get('from', None)
    item_name = args.get('item', None)

    # Nothing specified to take.
    if item_name is None:
        game.report(messagesTxt.malformed_take_request)
        return

    # Taking item already taken
    if container_name is not None and container_name.lower() == 'inventory':
        game.report(messageTxt.takingTakenItem(item_name))
        return

    # Take an item from a container
    if container_name is not None:
        source = container_name
        source_str = f"@{source}@"
        # Missing container
        if not game.hasItem(container_name):
            game.report(messageTxt.missingContainer(item_name, container_name))
            return
    # Take an item from the current room
    else:
        source = game.getPlayerLocation().name
        source_str = f"^{source}^"

    # Item not available to take
    item_location = game.getItemLocation(item_name)
    if item_location is None or item_location.lower() != source.lower():
        game.report(messageTxt.missingItem(item_name, source_str))

    else:
        item = game.getItem(item_name)
        # item taken
        if item.takeable:
            game.report(describe.take(item))
            game.addToInventory(item_name)

        # untakeable item
        else:
            game.report(messageTxt.untakeable(item_name))

def takeHelp():
    actionHelp("take", "Pick up an item and add it to your inventory")

