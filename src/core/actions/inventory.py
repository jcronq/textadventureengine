import src.text.textIO as txt

def inventory(game, args):
    items = [item.describe() for item in game.getInventoryContents()]
    item_txt = ["<br>".join(["*Inventory Contents:*"]+items)]
    txt.printGameBlock(item_txt)

