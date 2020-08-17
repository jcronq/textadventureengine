import sys
import yaml
import os
import uuid

import src.text.textIO as txt
import src.text.textUtils as txtUtil
import src.config.util as util
import src.text.describe as describe

import make.location as location
import make.item as item
import make.character as character
import make.gameMeta as game_meta

from src.config.load import GameLoader
from src.actions.examine import examine
from src.text.views import bashPrint as gamePrinter

game = util.chooseGame()
level = util.chooseLevel(game)

initializing = True
r_cmd = ['']
while r_cmd[0] != ':q':
    if not initializing:
        inputOptions = [
            {'key': 'cg', 'text':'change game'},
            {'key': 'cl', 'text':'change level'},
            {'key': 'el', 'text':'edit level'},
            {'key': 'me', 'text':'edit meta data'},
            {'key': ':q', 'text':'quit'},
        ]
        r_cmd = txt.promptInput('Game Editor', inputOptions)
    else:
        initializing = False
        r_cmd = ['el']

    if r_cmd[0] == 'cg':
        game = util.chooseGame()
        level = util.chooseLevel(game)
    elif r_cmd[0] == 'cl':
        level = util.chooseLevel(game)
    elif r_cmd[0] == 'me':
        game_meta.edit(game)
    elif r_cmd[0] == 'el':
        location_name = None

        cmd = ['']
        while cmd[0] != ':q':
            if location_name is not None:
                level_confs = util.loadLevelConfigs(game, level)
                playableGameObj = GameLoader(game).getGameObject()
                playableGameObj.setPlayerLocation(level_confs['locations'][location_name]['name'])
                examine(playableGameObj, {})
                gamePrinter(playableGameObj.getText())

                inputOptions = [
                    {'key': 'cl', 'text':'change location'},
                    {'key': 'ai', 'text':'add item'},
                    {'key': 'ac', 'text':'add character'},
                    {'key': ':q', 'text':'quit'},
                ]
                if len(level_confs['locations']) > 0:
                    inputOptions.append({'key': 'el', 'text':'edit location'})
                if len(playableGameObj.getRoomContents()) > 0:
                    inputOptions.append({'key': 'ei', 'text':'edit item'})
                if len(playableGameObj.getRoomCharacters()) > 0:
                    inputOptions.append({'key': 'ec', 'text':'edit character'})

                cmd = txt.promptInput('Level Editor', inputOptions)
            else:
                cmd = ['cl']

            if cmd[0] == 'cl':
                location_name = util.chooseLocation(game, level, allow_new_location = True)
                if location_name == 'New Location':
                    location_name = location.createNew(game, level)

            if cmd[0] == 'el':
                print('location.edit')
                location_name = location.edit(game, level, location_name)
            if cmd[0] == 'ei':
                item_name = util.chooseItem(game, level, location_name)
                item.edit(game, level, location_name, item_name)
            if cmd[0] == 'ai':
                item.createNew(game, level, location_name)
            if cmd[0] == 'ec':
                character_name = util.chooseCharacter(game, level, location_name)
                character.edit(game, level, location_name, character_name)
            if cmd[0] == 'ac':
                character.createNew(game, level, location_name)
            if cmd[0] == ':q':
                pass

    elif r_cmd[0] == ':q':
        pass

