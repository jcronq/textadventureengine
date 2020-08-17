import sys
import yaml
import os

import src.text.textIO as txt
import src.text.textUtils as txtUtil
import src.config.util as util

def createNew(game):
    print("Selecting Starting Location")
    level = util.chooseLevel(game)
    start_location = util.chooseStartingLocation(game, level)

    game_meta = {
        'initial_condition': {
            'start_location': start_location,
        }
    }

    util.saveGameMeta(game, game_meta)

def edit(game):
    game_meta = util.getGameMeta(game)
    if game_meta is None:
        createNew(game)
        return
    if 'initial_condition' not in game_meta:
        createNew(game)
        return
    if 'start_location' not in game_meta['initial_condition']:
        createNew(game)
        return

    inputOptions = [
        {'key': 's', 'text': 'start_location'},
        {'key': ':q', 'text': 'quit'},
    ]
    cmd = ['']
    while cmd[0] != ':q':
        print(yaml.dump(item_obj))
        cmd = util.promptInput('Meta Editor', inputOptions)

        if cmd[0]  == 's':
            print("Selecting Starting Location")
            level = util.chooseLevel(game)
            start_location = util.chooseStartingLocation(game, level)
            game_meta['initial_condition']['start_location'] = name

    util.saveGameObj('items', game, level, item_name, item_obj)

