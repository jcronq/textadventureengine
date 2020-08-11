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

def createNewConvo():
    game = util.chooseGame()
    level = util.chooseLevel(game)

    convo_uniq_name = util.chooseUniqueName('conversations', game, level)
    convo_config = util.loadConfig('conversations', game, level, convo_uniq_name)
    if convo_config is None:
        character_name = txt.getStr("Name", prompt_end=":", default=convo_uniq_name)
        [start_msg, start_rsp] = makeMessagePair(None)
        cur_msg = start_msg['uid']
        cur_opt = start_rsp['uid']

        conversation = {
            cur_msg: start_msg,
            cur_opt: start_rsp,
        }
    else:
        conversation = convo_config['conversation']
        character_name = convo_config['name']
        start_msg = conversation[convo_config['initial_msg']]
        cur_msg = start_msg['uid']
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
            {'key': 'rm', 'text':'Remove Option'},
            {'key': 'w', 'text':'write-to-file'},
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

        elif cmd[0] == 'w':
            util.saveGameObj('conversations', game, level, convo_uniq_name,
                {
                    'config':{
                        'initial_msg': start_msg['uid'],
                        'name': character_name,
                        'conversation': conversation
                    }
                })
        elif cmd[0] == 'quit':
            return

createNewConvo()
