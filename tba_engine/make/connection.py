import sys
import yaml
import os

import src.text.textIO as txt
import src.text.textUtils as txtUtil
import src.config.util as util

cardinal_map = {
    'north': 'south',
    'south': 'north',
    'east': 'west',
    'west': 'east',
    'up': 'down',
    'down': 'up',
}

def editor(game, level, location_name, connection_objs):
    if connection_objs is None:
        connection_objs = []
    print(connection_objs)
    inputOptions = [
        {'key': 'e', 'text': 'edit'},
        {'key': 'a', 'text': 'add'},
    ]
    cmd = txt.promptInput('Connection Editor', inputOptions)

    if cmd[0] == 'e':
        arg_id = txt.getOption('Which connection?', [connection['direction'] for connection in connection_objs])
        connection_objs[arg_id] = edit(game, connection_objs[arg_id], level, location_name)
    elif cmd[0] == 'a':
        connection_objs.append(createNew(game, level, location_name))
    return connection_objs

def createNewBlocker(game):
    state = txt.getStr('Block State')
    value = txt.getStr('Block State Value')
    failure_text = txt.getStr('Failure Text')
    success_text = txt.getStr('Success Text')
    travel_blockade = {
        'state': state,
        'value': value,
        'failure': failure_text,
        'success': success_text,
    }
    return travel_blockade

def editBlocker(game, blocker):
    cmd = ['']
    while cmd[0] != ':q':
        options = [
            {'key': 's', 'text':'replace state'},
            {'key': 'v', 'text':'replace value'},
            {'key': 'f', 'text':'repplace failure_text'},
            {'key': 'p', 'text':'replace success_text'},
            {'key': ':q', 'test': 'quit'},
        ]
        cmd = txt.promptInput('Blocker Editor', options)

        if cmd[0] == 's':
            blocker['state'] = txt.getStr('Block State')
        if cmd[0] == 'v':
            blocker['value'] = txt.getStr('Block State Value')
        if cmd[0] == 'f':
            blocker['failure'] = txt.getStr('Failure Text')
        if cmd[0] == 'p':
            blocker['success'] = txt.getStr('Success Text')

    return blocker

def addInboundConnectionToRef(game, from_ref, from_direction, location_ref):
    ref_obj = util.extractReference(location_ref)
    loc_config = util.loadConfigFromRef(game, location_ref)
    from_ref_obj = util.extractReference(from_ref)

    if from_direction in cardinal_map.keys():
        to_direction = cardinal_map[from_direction]
    else:
        to_direction = from_ref_obj['name']

    reflecting_connection = {
        'direction': to_direction,
        'location': from_ref,
        'travel_blockade': None,
        'travel_description': None,
    }
    if loc_config is None:
        loc_config = {
            'name': txtUtil.properNoun(ref_obj['obj_name'].replace('_', ' ')),
            'description': None,
            'examine_text': None,
            'connections': [],
        }

    """
    Every direction must be reflect.  If you came up a ladder,
    there must also be a down a ladder.  The location you end up
    in does not have to be the same location you came from though.
    ex) move from intro.square to intro.pub, then going back to square
        could take you to end_game.square
    """

    if loc_config.get('connections', None) is None:
        loc_config['connections'] = [reflecting_connection]
    else:
        outbound_connections = [conn['direction'] for conn in loc_config['connections']]
        if to_direction not in outbound_connections:
            loc_config['connections'].append(reflecting_connection)
    util.saveGameObjToRef(game, location_ref, loc_config)

def removeInboundConnectionFromRef(game, from_direction, from_ref, location_ref):
    from_ref_obj = util.extractReference(from_ref)
    loc_config = util.loadConfigFromRef(game, location_ref)
    if loc_config is None:
        print(f'ERROR: No reflection connection found at {location_ref}')
        return

    if from_direction in cardinal_map.keys():
        to_direction = cardinal_map[from_direction]
    else:
        to_direction = from_ref_obj['name']

    # breakpoint()
    con_to_rm = None
    for connection in loc_config.get('connections', []):
        if connection['direction'] == to_direction:
            con_to_rm = connection
    if con_to_rm is not None:
        loc_config['connections'].remove(con_to_rm)
    util.saveGameObjToRef(game, location_ref, loc_config)

def createNew(game, location_level, location_name):
    if txt.getYesNo('Cardinal Direction? (y/n)'):
        inputOptions = [
            {'key': 'n', 'text': 'north'},
            {'key': 's', 'text': 'south'},
            {'key': 'e', 'text': 'east'},
            {'key': 'w', 'text': 'west'},
            {'key': 'u', 'text': 'up'},
            {'key': 'd', 'text': 'down'},
        ]
        cmd = txt.promptInput('Cardinal Directions', inputOptions)
        direction = [opt['text'] for opt in inputOptions if opt['key'] == cmd[0]][0]

    to_text = txt.getStr("Travel to Description")

    if txt.getYesNo('Has Blocker? (y/n) '):
        travel_blockade = createNewBlocker(game)
    else:
        travel_blockade = None

    # Allow inter-level connections (level changes smoothly via travel)
    location_ref = getLocationRef(game, location_level)
    from_ref = util.getReference('locations', location_level, location_name)
    addInboundConnectionToRef(game, from_ref, direction, location_ref)

    return {
        'direction': direction,
        'location': location_ref,
        'travel_blockade': travel_blockade,
        'travel_description': to_text,
    }

def getLocationRef(game, location_level):
    if txt.getYesNo("Connecting to same level? (y/n)"):
        level = location_level
    else:
        level = util.chooseLevel(game)
    location = util.chooseLocation(game, level, allow_new_location=True)
    if location == 'New Location':
        location = txt.getStr('Location Name (new)')
    location_ref = util.getReference('locations', level, location)
    return location_ref

def edit(game, connection_obj, location_level, location_name):
    cmd = ['']
    while cmd[0] != ':q':
        inputOptions = [
            {'key': 'di', 'text': 'change direction name'},
            {'key': 'l', 'text': 'change location reference'},
            {'key': 'b', 'text': 'change blockade'},
            {'key': 'de', 'text': 'change travel description'},
            {'key': ':q', 'text': 'Done editing'}
        ]
        print(yaml.dump(connection_obj))
        cmd = txt.promptInput("Connection Editor", inputOptions)
        if cmd[0] == 'di':
            print("DON'T CHANGE A CARDINAL DIRECTION, if you must, edit it manually in the configs")
            connection_obj['direction'] = txt.getStr("Direction")
        elif cmd[0] == 'l':
            current_ref = connection_obj['location']
            location_ref = getLocationRef(game, location_level)
            from_ref = util.getReference('locations', location_level, location_name)

            if current_ref is not None:
                removeInboundConnectionFromRef(game, connection_obj['direction'], from_ref, current_ref)
            addInboundConnectionToRef(game, from_ref, connection_obj['direction'], location_ref)

            connection_obj['location'] = location_ref
        elif cmd[0] == 'b':
            connection_obj['travel_blockade'] = editBlocker(game, connection_obj['travel_blockade'])
        elif cmd[0] == 'de':
            connection_obj['travel_description'] = txt.getStr('Travel Description')

    return connection_obj

