def drop(game, args):
    obj_to_drop = args.get('item', None)
    if obj_to_drop is None:
        game.report("I don't understand what you want me to drop.")
        return
    inventory_contents = [item.name.lower() for item in
                          game.getInventoryContents()]
    if obj_to_drop.lower() not in inventory_contents:
        game.report(f"I don't have a *{obj_to_drop}* in my inventory.")
    else:
        game.dropItem(obj_to_drop)
        item = game.getItem(obj_to_drop)
        drop_txt = []
        drop_txt += [item.drop_text]
        drop_txt += [f"{obj_to_drop} *dropped*"]
        game.report(drop_txt)
