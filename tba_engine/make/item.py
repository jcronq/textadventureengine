import sys
import yaml
import os

import src.text.textIO as txt
import src.text.textUtils as txtUtil
import src.config.util as util

def createNew(game, level, location=None):
    item_name = util.chooseUniqueName('items', game, level)
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
        'start_location': start_location+'.name',
        'examine_text': examine_text,
        'takeable': is_takeable,
        'take_text': take_text,
        'drop_text': drop_text,
        'is_container': is_container
    }

    util.saveItem('items', game, level, location, item_name, item_obj)

def edit(game, level, location, item_name):
    item_obj = util.loadItem(game, level, location, item_name)
    original_location = util.extractReference(item_obj['start_location'])['obj_name']
    original_name = item_obj['name']
    inputOptions = [
        {'key': 'n', 'text': 'name'},
        {'key': 'd', 'text': 'description'},
        {'key': 'e', 'text': 'examine'},
        {'key': 'l', 'text': 'location'},
        {'key': 't', 'text': 'is_takeable'},
        {'key': 'c', 'text': 'is_container'},
        {'key': ':q', 'text': 'quit'},
    ]
    cmd = ['']
    while cmd[0] != ':q':
        print(yaml.dump(item_obj))

        cmd = txt.promptInput('Item Editor', inputOptions)

        if cmd[0]  == 'n':
            if len(cmd) > 1:
                name = ' '.join(cmd[1:])
            else:
                name = util.chooseUniqueName('items', game, level)
            item_obj['name'] = name

        elif cmd[0] == 'd':
            if len(cmd) > 1:
                description = ' '.join(cmd[1:])
            else:
                description = txt.getStr('Description')
            item_obj['description'] = description

        elif cmd[0] == 'e':
            if len(cmd) > 1:
                examine = ' '.join(cmd[1:])
            else:
                examine = txt.getStr('Examine')
            item_obj['examine'] = examine

        elif cmd[0] == 'l':
            item_obj['start_location'] = util.chooseStartingLocation(game, level)

        elif cmd[0] == 't':
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

        elif cmd[0] == 'c':
            item_obj['is_container'] = txt.getYesNo("Is Container?\n> ")

    location = util.extractReference(item_obj['start_location'])['obj_name']
    if original_name != item_obj['name'] or original_location != location:
        util.removeItem(game, level, original_location, original_name)
    util.saveItem(game, level, location, item_obj['name'], item_obj)

