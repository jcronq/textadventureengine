import sys
import yaml
import os
import uuid

import src.text.textIO as txt
import src.text.textUtils as txtUtil
import src.config.util as util
import src.text.describe as describe

def makeNewNpcMessage(parent):
    npc_uid = str(uuid.uuid4())
    npc_message_str = txt.getStr("NPC_Response")
    npc_message = {
        'uid':  npc_uid,
        'type': 'npc',
        'txt':  npc_message_str,
        'next': None,
        'parent': parent,
    }
    return npc_message

def makeNewOptMessage(parent):
    opt_uid = str(uuid.uuid4())
    opt_message = {
        'uid':  opt_uid,
        'type': 'player-opt',
        'opt':[],
        'parent': parent,
    }
    return opt_message

def makeMessagePair(parent):
    msg = makeNewNpcMessage(parent)
    rsp = makeNewOptMessage(msg['uid'])
    msg['next'] = rsp['uid']
    return [msg, rsp]

def getMsgOpt(conversation, cur_msg_obj):
    next_msg = cur_msg_obj.get('next', None)
    return conversaiont.get(next_msg, None)

def edit(game, level, char_name, location):
    location_ref = util.getReference('locations', level, location)

    convo_config = util.loadLocalizedGameObj('conversations', game, level,
                                             location, char_name)
    conversation = convo_config['conversation']
    start_msg = conversation[convo_config['initial_msg']]
    cur_msg = start_msg['uid']
    cur_opt = conversation[cur_msg]['next']

    convo_config['conversation'] = conversationTreeEditor(conversation)

    util.saveLocalizedGameObj('conversations', game, level, location, char_name, convo_config)

def editor(game, level, char_name, conversations):
    options = [
        {'key': 'c', 'text': 'create new'},
        {'key': 'e', 'text': 'bind existing'},
    ]
    cmd = txt.promptInput('Conversation Editor', options)
    if cmd[0] == 'e':
        choice = txt.getOption('Select Conversation', conversations)

        options = [
            {'key': 'l', 'text': 'location'},
            {'key': 'co', 'text': 'conversation'},
        ]
        s_cmd = txt.promptInput('Conversation Editor', options)
        if s_cmd[0] == 'l':
            [old_loc, char_name] = conversations[choice].split('-')
            new_loc = util.chooseLocation(game, level, exclude=[old_loc])
            game_obj = util.loadLocalizedGameObj('conversations',
                                     game, level, old_loc, char_name)

            game_obj['location'] = new_loc
            util.removeLocalizedGameObj('conversations',
                                        game, level, old_loc, char_name)
            util.saveLocalizedGameObj('conversations',
                                     game, level, new_loc, char_name, game_obj)
            conversations.remove(conversations[choice])
            conversations.append(util.getLocalizedReference('conversations',
                                                level, location, char_name))
        if s_cmd[0] == 'co':
            [location, char_name] = conversations[choice].split('-')
            edit(game, level, char_name, location)
    elif cmd[0] == 'c':
        conversations.append(createNew(game, level, char_name))

    return conversations

def createNew(game, level, char_name, location=None):
    if location is None:
        location = util.chooseAnyLocation(allow_new_locations=False)
    [start_msg, start_rsp] = makeMessagePair(None)
    cur_msg = start_msg['uid']
    cur_opt = start_rsp['uid']

    conversation = {
        cur_msg: start_msg,
        cur_opt: start_rsp,
    }

    conversation = conversationTreeEditor(conversation, char_name, cur_msg)
    convo_name = f"{location}-{char_name}"
    convo_config = {
        'initial_msg': start_msg['uid'],
        'name': char_name,
        'location': location,
        'conversation': conversation,
    }

    util.saveLocalizedGameObj('conversations', game, level, location,
                                     char_name, convo_config)
    return util.getLocalizedReference('conversations', level, location,
                                     char_name)

def conversationTreeEditor(conversation, character_name, cur_msg):
    cur_opt = conversation[cur_msg]['next']
    cont = True
    while cont:
        output = txt.formatHtmlBlock(describe.conversationMessage(
                character_name,
                conversation[cur_msg]['txt'],
                conversation[cur_opt]['opt']
            ))
        for block in output:
            print(block.replace('<br>', '\n'))

        inputOptions = [
            {'key': 's', 'text':'select'},
            {'key': 'b', 'text':'back'},
            {'key': 'e', 'text':'Edit'},
            {'key': 'a', 'text':'Add Option'},
            {'key': 'rm','text':'Remove Option'},
            {'key': 'w', 'text':'write-to-file'},
            {'key': ':q','text':'quit'},
        ]
        cmd = txt.promptInput(' ', inputOptions)
        print(cmd)

        if cmd[0] == 's':
            if conversation[cur_opt]['opt'][int(cmd[1])].get('next', None) not in conversation:
                [msg, rsp] = makeMessagePair(cur_opt)
                conversation[cur_opt]['opt'][int(cmd[1])]['next'] = msg['uid']

                cur_msg = msg['uid']
                cur_opt = rsp['uid']

                conversation[cur_msg] = msg
                conversation[cur_opt] = rsp
            else:
                cur_msg = conversation[cur_opt]['opt'][int(cmd[1])]['next']
                cur_opt = conversation[cur_msg]['next']

        elif cmd[0] == 'b':
            if conversation[cur_msg]['parent'] is not None:
                cur_opt = conversation[cur_msg]['parent']
                cur_msg = conversation[cur_opt]['parent']

        elif cmd[0] == 'e':
            if len(cmd) == 1:
                print(conversation[cur_msg]['txt'])
                new_response = txt.getStr("Response", prompt_end=":")
                conversation[cur_msg]['txt'] = new_response

            else:
                print(conversation[cur_opt]['opt'][int(cmd[1])]['txt'])
                new_response = txt.getStr("Response", prompt_end = ":")
                conversation[cur_opt]['opt'][int(cmd[1])]['txt'] = new_response

        elif cmd[0] == 'a':
            if len(cmd) == 1:
                new_response = txt.getStr("Response", prompt_end = ":")
            else:
                new_response = " ".join(cmd[1:])
            conversation[cur_opt]['opt'].append({
                'txt':new_response,
                'next':None,
            })

        elif cmd[0] == 'rm':
            del conversation[cur_opt]['opt'][cmd[1]]

        elif cmd[0] == ':q':
            return conversation

#useful later
