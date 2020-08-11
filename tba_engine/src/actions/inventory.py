import src.text.describe as describe

def inventory(game, args):
    game.report(describe.inventory(game.getInventoryContents()))

