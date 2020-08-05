def inventory(game, args):
    items = [item.describe() for item in game.getInventoryContents()]
    item_txt = ["<br>".join(["*Inventory Contents:*"]+items)]
    game.report(item_txt)

