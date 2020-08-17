import sys
import yaml
import os

import src.text.textIO as txt
import src.text.textUtils as txtUtil
import src.config.util as util

import make.convo as convo

def createNew(game, level, location=None):
    char_name = util.chooseUniqueName('characters', game, level)

    if location is None:
        start_location = util.chooseStartingLocation(game, level)
    else:
        start_location = util.getReference('locations', level, location)
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
        'name': char_name,
        'description': description,
        'start_location': start_location+'.name',
        'examine_text': examine_text,
        'takeable': is_takeable,
        'take_text': take_text,
        'drop_text': drop_text,
        'is_container': is_container,
        'dialogue': [],
    }

    if txt.getYesNo("Add conversation? (y/n)\n> "):
        char_obj['dialogue'].append(
            convo.createNew(game, level, char_name, location)
        )

    util.saveGameObj('characters', game, level, char_name, char_obj)

def edit(game, level, location, character_name):
    char_obj = util.loadConfig('characters', game, level, character_name)
    inputOptions = [
        {'key': 'n', 'text': 'name'},
        {'key': 'd', 'text': 'description'},
        {'key': 'l', 'text': 'location'},
        {'key': 'e', 'text': 'examine'},
        {'key': 't', 'text': 'take'},
        {'key': 'ic', 'text': 'is_container'},
        {'key': 'cv', 'text': 'convo'},
        {'key': ':q', 'text': 'quit'},
    ]

    cmd = ['']
    while cmd[0] != ':q':
        print(yaml.dump(char_obj))
        cmd = txt.promptInput('Character Editor', inputOptions)

        if cmd[0] == 'n':
            if len(cmd) > 1:
                name = ' '.join(cmd[1:])
            else:
                name = util.chooseUniqueName('characters', game, level)
            char_obj['name'] = name

        elif cmd[0] == 'd':
            if len(cmd) > 1:
                description = ' '.join(cmd[1:])
            else:
                description = txt.getStr('Description')
            char_obj['description'] = description

        elif cmd[0] == 'e':
            if len(cmd) > 1:
                examine = ' '.join(cmd[1:])
            else:
                examine = txt.getStr('Examine')
            char_obj['examine'] = examine

        elif cmd[0] == 'l':
            char_obj['start_location'] = util.chooseStartingLocation(game, level)

        elif cmd[0] == 't':
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

        elif cmd[0] == 'ic':
            char_obj['container'] = txt.getYesNo("Is Container?\n> ")

        elif cmd[0] == 'cv':
            convo.editor(game, level, char_obj['name'], char_obj['dialogue'])

    util.saveGameObj('characters', game, level, char_obj['name'], char_obj)

