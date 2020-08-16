import sys
import yaml
import os

import src.text.textIO as txt
import src.text.textUtils as txtUtil
import src.config.util as util

def createNew(game, level, location=None):
    item_uniq_name = util.chooseUniqueName('items', game, level)
    item_name = txt.getStr("Name", prompt_end = ":", default=item_uniq_name)
    if location is None:
        start_location = util.chooseStartingLocation(game, level)
    else:
        start_location = util.getReference('locations', level, location)
    description = txt.getStr("Description", prompt_end = ":")
    examine_text = txt.getStr("Examine Text", prompt_end = ":")
    is_container = txt.getYesNo("Is a container?\n> ")
    is_takeable = txt.getYesNo("Is takeable?\n> ")
    if is_takeable:
        take_text = txt.getStr("Take Text", prompt_end = ":")
        drop_text = txt.getStr("Drop Text", prompt_end = ":")
    else:
        take_text = None
        drop_text = None

    item_obj = {
        'name': item_name,
        'description': description,
        'start_location': start_location,
        'examine_text': examine_text,
        'takeable': is_takeable,
        'take_text': take_text,
        'drop_text': drop_text,
        'is_container': is_container
    }

    util.saveConf('items', game, level, item_name, item_obj)

def edit(game, level, location, item_name):
    item_obj = util.loadItem('items', game, level, location, item_name)
    inputOptions = [
        {'key': 'name', 'text': ''},
        {'key': 'description', 'text': ''},
        {'key': 'examine', 'text': ''},
        {'key': 'location', 'text': ''},
        {'key': 'take', 'text': ''},
        {'key': 'container', 'text': ''},
        {'key': ':q', 'text': 'quit'},
    ]
    cmd = ['']
    while cmd[0] != ':q':
        print(yaml.dump(item_obj))

        if cmd[0]  == 'name':
            if len(cmd) > 1:
                name = ' '.join(cmd[1:])
            else:
                name = util.chooseUniqueName('items', game, level)
            item_obj['name'] = name

        elif cmd[0] == 'description':
            if len(cmd) > 1:
                description = ' '.join(cmd[1:])
            else:
                description = txt.getStr('Description')
            item_obj['description'] = description

        elif cmd[0] == 'examine':
            if len(cmd) > 1:
                examine = ' '.join(cmd[1:])
            else:
                examine = txt.getStr('Examine')
            item_obj['examine'] = examine

        elif cmd[0] == 'location':
            item_obj['start_location'] = util.chooseStartingLocation(game, level)

        elif cmd[0] == 'take':
            is_takeable = txt.getYesNo("Is takeable?\n> ")
            if is_takeable:
                take_suggestion = item_obj.get('take_text', '')
                drop_suggestion = item_obj.get('drop_text', '')
                item_obj['take_text'] = txt.getStr("Take Text", take_suggestion)
                item_obj['drop_text'] = txt.getStr("Drop Text", drop_suggestion)
            elif not is_takeable:
                item_obj['take_text'] = None
                item_obj['drop_text'] = None
            item_obj['takeable'] = is_takeable

        elif cmd[0] == 'container':
            item_obj['is_container'] = txt.getYesNo("Is Container?\n> ")

    util.saveConf('items', game, level, item_name, item_obj)

