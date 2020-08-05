def examine(game, args, debug=False):
    obj_name_to_examine = args.get('item', None)
    if obj_name_to_examine is None:
        obj_name_to_examine = game.getPlayerLocation().name
        obj_to_examine = game.getLocation(obj_name_to_examine)
    else:
        obj_to_examine = game.getItem(obj_name_to_examine)
    inventory_contents = [item.name.lower() for item in game.getInventoryContents()]
    room_contents = [item.name.lower() for item in game.getRoomContents()]
    current_room = game.getPlayerLocation().name.lower()
    if obj_to_examine is None or (\
        obj_to_examine.name.lower() not in inventory_contents \
        and obj_to_examine.name.lower() not in room_contents \
        and obj_to_examine.name.lower() != current_room):
        game.report([f"Hmm... Nope, I don't see any *{obj_name_to_examine}* here."])
    elif obj_to_examine.name.lower() == current_room:
        txt_block = getLocationTextBlock(game)
        game.report(txt_block)
    else:
        txt_block = getItemTextBlock(game, obj_to_examine)
        game.report(txt_block)

def getItemTextBlock(game, item):
    item_txt = []
    item_txt.append(item.examine())
    if item.is_container:
        sub_items = game.getItemsInLocation(item.name)
        item_description = ["*Items:*"]+list(['- '+item.describe()
                                          for item in sub_items])
        item_txt += ["<br>".join(item_description)]
    return item_txt

def getLocationTextBlock(game):
    location_txt = []
    current_location = game.getPlayerLocation()
    location_txt.append(current_location.examine())
    items = game.getItemsInLocation(current_location.name)
    item_description = ["*Notable Objects:*"]+list(['- '+item.describe()
                                          for item in items])
    print(len(items))
    if len(items) == 0:
        item_description = ["Nothing noteworthy here."]
    else:
        item_description = ["*Notable Objects:*"]+list(['- '+item.describe()
                                              for item in items])
    location_txt += ["<br>".join(item_description)]
    return location_txt

