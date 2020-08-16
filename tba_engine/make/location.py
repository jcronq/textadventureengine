import sys
import yaml
import os

import src.text.textIO as txt
import src.text.textUtils as txtUtil
import src.config.util as util
import make.connection as connection

def createNew(game, level):
    location_name = util.chooseUniqueName('locations', game, level)
    description = txt.getStr("Description", prompt_end = ":")
    examine_text = txt.getStr("Examine Text", prompt_end = ":")

    location_obj = {
        'name': location_name,
        'description': description,
        'examine_text': examine_text,
        'connections': [],
    }

    util.saveGameObj('locations', game, level, location_name, location_obj)
    return location_name

def edit(game, level, location):
    print(game, level, location)
    location_obj = util.loadConfig('locations', game, level, location)
    original_name = location_obj['name']
    cmd = ['']
    options=[
        {'key': 'd', 'text': 'description'},
        {'key': 'c', 'text': 'connections'},
        {'key': 'e', 'text': 'examine_text'},
        {'key': 'n', 'text': 'name'},
        {'key': ':q', 'text': 'quit'},
    ]
    while cmd[0] != ':q':
        print(yaml.dump(location_obj))
        cmd = txt.promptInput('Location Editor', options)

        if cmd[0] == 'n':
            location_obj['name'] = util.chooseUniqueName('locations', game, level)
        elif cmd[0] == 'd':
            location_obj['description'] = txt.getStr('description')
        elif cmd[0] == 'e':
            location_obj['examine_text'] = txt.getStr('examine_txt')
        elif cmd[0] == 'c':
            location_obj['connections'] = connection.editor(game, level, location_obj['name'], location_obj['connections'])

    if original_name != location_obj['name']:
        util.removeGameObj('locations', game, level, original_name, location_obj)
    util.saveGameObj('locations', game, level, location_obj['name'], location_obj)

    return location_obj['name']

