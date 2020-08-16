import sys
import yaml
import os

import src.text.textIO as txt
import src.text.textUtils as txtUtil
import src.config.util as util

def createNew(game, level, location=None):
    char_name = util.chooseUniqueName('characters', game, level)

    if location is None:
        start_location = util.chooseStartingLocation(game, level)
    else:
        start_location = util.getReference('characters', level, location)
    description = txt.getStr("Description", prompt_end = ":")
    examine_text = txt.getStr("Examine Text", prompt_end = ":")
    is_container = txt.getYesNo("Is a container? (y/n)\n> ")
    is_takeable = txt.getYesNo("Is takeable? (y/n)\n> ")

    if is_takeable:
        take_text = txt.getStr("Take Text", prompt_end = ":")
        drop_text = txt.getStr("Drop Text", prompt_end = ":")
    else:
        take_text = None
        drop_text = None

    char_obj = {
        'name': name,
        'description': description,
        'start_location': start_location,
        'examine_text': examine_text,
        'takeable': is_takeable,
        'take_text': take_text,
        'drop_text': drop_text,
        'is_container': is_container,
        'dialogue': None,
    }

    if txt.getYesNo("Add conversation? (y/n)\n> "):
        char_obj[key] = util.chooseConversation(game, level)

    util.saveConf(char_obj)

def edit(game, level, location, character_name):
    char_obj = util.loadConfig('characters', game, level, character_name)
    inputOptions = [
        {'key': 'name', 'text': ''},
        {'key': 'description', 'text': ''},
        {'key': 'location', 'text': ''},
        {'key': 'examine', 'text': ''},
        {'key': 'take', 'text': ''},
        {'key': 'container', 'text': ''},
        {'key': 'convo', 'text': ''},
    ]

    cmd = ['']
    while cmd[0] != ':q':
        print(yaml.dump(char_obj_defn))
        txt.promptInput('Character Editor', inputOptions)

        if cmd[0] == 'name':
            if len(cmd) > 1:
                name = ' '.join(cmd[1:])
            else:
                name = util.chooseUniqueName('characters', game, level)
            char_obj['name'] = name

        elif cmd[0] == 'description':
            if len(cmd) > 1:
                description = ' '.join(cmd[1:])
            else:
                description = txt.getStr('Description')
            char_obj['description'] = description

        elif cmd[0] == 'examine':
            if len(cmd) > 1:
                examine = ' '.join(cmd[1:])
            else:
                examine = txt.getStr('Examine')
            char_obj['examine'] = examine

        elif cmd[0] == 'location':
            char_obj['start_location'] = util.chooseStartingLocation(game, level)

        elif cmd[0] == 'take':
            is_takeable = txt.getYesNo("Is takeable?\n> ")
            if is_takeable:
                take_suggestion = char_obj.get('take_text', '')
                drop_suggestion = char_obj.get('drop_text', '')
                char_obj['take_text'] = txt.getStr("Take Text", take_suggestion)
                char_obj['drop_text'] = txt.getStr("Drop Text", drop_suggestion)
            elif not is_takeable:
                char_obj['take_text'] = None
                char_obj['drop_text'] = None
            char_obj['takeable'] = is_takeable

        elif cmd[0] == 'container':
            char_obj['container'] = txt.getYesNo("Is Container?\n> ")

        elif key == 'dialogue':
            char_obj[key] = util.chooseConversation(game, level)
        else:
            char_obj[key] = txt.getStr(key)

    util.saveConf('characters', game, level, item_name, item_obj)

