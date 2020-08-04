from src.core.actions.help import actionHelp
import src.text.textIO as txt

def take(game, args={}):
    container_name = args.get('from', None)
    item_name = args.get('item', None)
    if item_name is None:
        txt.printGameBlock("I don't understand what you want me to take.")
        return

    if container_name is not None and container_name.lower() == 'inventory':
        txt.printGameBlock("Err... and put it where exactly? If you want to *drop* the item... well that's always an option.")
        return

    if container_name is not None:
        source = container_name
        if not game.hasItem(container_name):
            txt.printGameBlock(f"I can't find a *{source}* to take *{item_name}* from!")
            return
    else:
        source = game.getPlayerLocation().name

    item_location = game.getItemLocation(item_name)
    print(item_location, source)
    if item_location is None or item_location.lower() != source.lower():
        txt.printGameBlock(f"Hmm... There's no *{item_name}* in *{source}*.")
    else:
        game.addToInventory(item_name)
        item = game.getItem(item_name)
        if item.takeable:
            take_text = []
            take_text.append(item.take_text)
            take_text.append(f"*{item.name} added to inventory.*")
            txt.printGameBlock(take_text)
        else:
            txt.printGameBlock(f"I don't think I can take *{item.name}*")

def takeHelp():
    actionHelp("take", "Pick up an item and add it to your inventory")

