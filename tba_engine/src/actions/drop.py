import src.text.messages as messageTxt
import src.text.describe as describe

def drop(game, args):
    obj_to_drop = args.get('item', None)

    # Drop item not specified
    if obj_to_drop is None:
        game.report(messageTxt.malformed_drop_request)
        return

    inventory_contents = [item.name.lower() for item in
                          game.getInventoryContents()]

    # Item no in inventory
    if obj_to_drop.lower() not in inventory_contents:
        game.report(messageTxt.itemNotInInventory(obj_to_drop))
    else:
        drop_obj = game.getItem(obj_to_drop)
        game.dropItem(obj_to_drop)
        game.report(describe.drop(drop_obj))

