import src.text.examine as examineTxt
import src.text.messages as messagesTxt

def examine(game, args, debug=False):
    obj_name = args.get('item', None)
    obj_to_examine = getObjectToExamine(game, obj_name)

    inventory_contents = [item.name.lower() for item in game.getInventoryContents()]
    room_contents = [item.name.lower() for item in game.getRoomContents()]
    current_room = game.getPlayerLocation().name.lower()

    # object not found
    if obj_to_examine is None or (\
        obj_to_examine.name.lower() not in inventory_contents \
        and obj_to_examine.name.lower() not in room_contents \
        and obj_to_examine.name.lower() != current_room):
        game.report(messagesTxt.missingObj(obj_name))

    # Examining current room
    elif obj_to_examine.name.lower() == current_room:
        txt_block = getLocationTextBlock(game)
        game.report(txt_block)
        game.setExamined(obj_to_examine.name, 'location')

    # Examining item
    else:
        txt_block = getItemTextBlock(game, obj_to_examine)
        game.report(txt_block)
        game.setExamined(obj_to_examine.name, 'item')

def getObjectToExamine(game, obj_name):
    if obj_name is None or obj_name.strip() == '':
        return game.getPlayerLocation()
    else:
        return game.getItem(obj_name)

def getItemTextBlock(game, item):
    sub_items = game.getItemsInLocation(item.name)
    return examineTxt.item(item, sub_items)

def getLocationTextBlock(game):
    current_location = game.getPlayerLocation()
    items = game.getItemsInLocation(current_location.name)
    return examineTxt.location(current_location, items)

