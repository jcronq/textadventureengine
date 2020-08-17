import sys
import yaml
import os
import re

import src.text.textIO as txt
import src.text.textUtils as txtUtil

GAMES_ROOT = './games'

NONE_FILTER = lambda x: x is not None

OBJ_TYPES = [
    'items',
    'characters',
    'locations',
    'conversations',
]

def flatten(list_of_lists):
    flat_list = []
    for sublist in list_of_lists:
        for item in sublist:
            flat_list.append(item)
    return flat_list

def getGameRoot(game):
    return f'{GAMES_ROOT}/{game}'

def getLevelRoot(game, level):
    return f'{getGameRoot(game)}/{level}'

def getObjRoot(obj_type, game, level):
    return f'{getLevelRoot(game, level)}/{obj_type}.d'

def getMetaFile(game):
    return f'{GAMES_ROOT}/{game}/game_meta.yaml'

def getGames():
    return os.listdir(GAMES_ROOT)

def getLevels(game):
    game_root = getGameRoot(game)
    levels = os.listdir(game_root)
    level_names = list(filter(lambda f: 'yaml' not in f, levels))
    return level_names

def getGameObjects(obj_type, game, level):
    try:
        query_result = os.listdir(getObjRoot(obj_type, game, level))
        game_objs = [f_name.split('.')[0].lower() for f_name in query_result]
        return game_objs
    except:
        return []

def getLocations(game, level):
    return getGameObjects('locations', game, level)

def getItems(game, level):
    return getGameObjects('items', game, level)

def getConversations(game, level):
    return getGameObjects('conversations', game, level)

def getCharacters(game, level):
    return getGameObjects('characters', game, level)

def getObjFileName(obj_type, game, level, obj_name):
    file_name = f"{getObjRoot(obj_type, game, level)}/{obj_name.replace(' ','_')}.yaml"
    return file_name

def getGameMeta(game):
    meta_file_name = getMetaFile(game)
    try:
        with open(meta_file_name, 'r') as f:
            contents = f.read()
            game_meta = yaml.full_load(contents)
            return game_meta
    except:
        return None

def saveGameMeta(game, meta_obj):
    meta_file_name = getMetaFile(game)
    with open(meta_file_name, 'w') as f:
        f.write(yaml.dump(meta_obj))

def getGameStartLocation(game):
    try:
        meta = getGameMeta(game)
        start_location = extractReference(meta['initial_condition']['start_location'])
        return start_location[-1]
    except:
        return None

def getKeyEditOptions(game_obj):
    options = [{'key': opt, 'text': ''} for opt in game_obj.keys()]
    options.append({'key': ':q', 'text': ''})
    return options

def extractReference(raw_ref):
    ref_array = extractReferenceToArray(raw_ref)
    return {
        'level': ref_array[0],
        'obj_type': ref_array[1],
        'obj_name': ref_array[2],
    }

def extractReferenceToArray(raw_ref):
    ref_regex = re.compile(r'<(.+)>')
    matches = ref_regex.findall(raw_ref)
    if len(matches) == 0:
        return []
    else:
        return matches[0].split('.')

def removeGameObj(obj_type, game, level, obj_name):
    obj_name = obj_name.replace(' ', '_')
    root = getObjRoot(obj_type, game, level)
    os.remove(f'{root}/{obj_name}.yaml')

def saveGameObjToRef(game, ref, obj):
    ref_obj = extractReference(ref)
    saveGameObj(ref_obj['obj_type'], game, ref_obj['level'], ref_obj['obj_name'], obj)

def saveGameObj(obj_type, game, level, obj_name, obj):
    obj_name = obj_name.replace(' ', '_').lower()
    root = getObjRoot(obj_type, game, level)
    with open(f'{root}/{obj_name}.yaml', 'w') as f:
        f.write(yaml.dump(obj))

def loadConfigFromRef(game, obj_ref):
    obj_parts = extractReference(obj_ref)
    return loadConfig(obj_parts['obj_type'], game, obj_parts['level'],
                      obj_parts['obj_name'])

def removeLocalizedGameObj(obj_type, game, level, location, item_name):
    location = location.lower().replace(' ', '_')
    item_name = item_name.lower().replace(' ', '_')
    obj_name = f'{location}-{item_name}'
    removeGameObj(obj_type, game, level, obj_name)

def removeItem(game, level, location, item_name):
    removeLocalizedGameObj('items', game, level, location, item_name)

def saveItem(game, level, location, item_name, item_obj):
    saveLocalizedGameObj('items', game, level, location, item_name, item_obj)

def saveLocalizedGameObj(obj_type, game, level, location, item_name, item_obj):
    location = location.lower().replace(' ', '_')
    item_name = item_name.lower().replace(' ', '_')
    saveGameObj(obj_type, game, level, f'{location}-{item_name}', item_obj)
    return f'{location}-{item_name}'

def loadItems(game, level, location):
    location = location.lower().replace(' ', '_')
    item_names = getItems(game, level)
    items = list(filter(lambda item_name: location in item_name, item_names))
    return [loadConfig('items', game, level, item_name) for item_name in items]

def loadItem(game, level, location, item_name):
    loadLocalizedGameObj('items', game, level, location, item_name)

def loadLocalizedGameObj(obj_type, game, level, location, item_name):
    location = location.lower().replace(' ', '_')
    item_name = item_name.lower().replace(' ', '_')
    return loadConfig(obj_type, game, level, f'{location}-{item_name}')

def loadConfig(obj_type, game, level, obj_name):
    flat_name = obj_name.replace(' ', '_').lower()
    file_name = getObjFileName(obj_type, game, level, flat_name)
    try:
        with open(file_name, 'r') as f:
            content = f.read()
            # obj = yaml.full_load(content)
            conf = yaml.full_load(content)
            # conf = obj['config']
            conf['uniq_name'] = obj_name
            return conf
    except:
        return None

def loadConfigList(obj_type, game, level, obj_list):
    return dict([(obj_name, loadConfig(obj_type, game, level, obj_name))
        for obj_name in obj_list])

def loadLevelConfigs(game, level):
    obj_names = dict([
        (obj_type, getGameObjects(obj_type, game, level))
        for obj_type in OBJ_TYPES
    ])
    obj_configs = dict([
        (obj_type, loadConfigList(obj_type, game, level, obj_list))
        for obj_type, obj_list in obj_names.items()
    ])
    return obj_configs

def getContainers(game, level):
    items = getItems(game, level)
    item_configs = [loadConfig('items', game, level, item) for item in items]
    if None in item_configs:
        raise Exception("Error could not load config for one of the following", items)
    container_filter = lambda config: config.is_container
    container_configs = list(filter(container_filter, item_configs))
    containers_stack = [list(config.keys()) for config in container_configs]
    containers = flatten(containers_stack)
    return(containers)

def makeGame():
    game_name = txt.getStr("Name of the Game?")
    game_root = getGameRoot(game_name.replace(' ', '_'))
    if not os.path.exists(game_root):
        os.mkdir(game_root)
    return game_name

def makeLevel(game):
    level = txt.getStr("Name of the Level?")
    level_root = getLevelRoot(game, level.replace(' ', '_'))
    if not os.path.exists(level_root):
        os.mkdir(level_root)
    game_dirs = [
        getObjRoot('conversations', game, level),
        getObjRoot('items', game, level),
        getObjRoot('locations', game, level),
        getObjRoot('characters', game, level)
    ]
    for directory in game_dirs:
        if not os.path.exists(directory):
            os.mkdir(directory)
    return level

def chooseGame():
    games = getGames()
    prompt = "Choose a game"
    options = [txtUtil.properNoun(game.replace('_', ' ')) for game in games]
    options += ["New Game"]
    choice = txt.getOption(prompt, options)
    if choice < len(games):
        return games[choice]
    else:
        return makeGame()

def chooseLevel(game):
    levels = getLevels(game)
    prompt = "Choose Level"
    options = levels + ["New Level"]
    choice = txt.getOption(prompt, options)
    if choice < len(levels):
        return levels[choice]
    else:
        return makeLevel(game)

def chooseUniqueName(obj_type, game, level):
    existing_objs = getGameObjects(obj_type, game, level)
    existing_names = [obj.replace('_', ' ').lower() for obj in existing_objs]
    item_uniq_name = txt.getStr("Unique Name")
    while item_uniq_name.lower().replace('_', ' ') in existing_names:
        item_uniq_name = txt.getStr(f"{item_uniq_name} is already taken. Please choose another\nUnique Name")
    return item_uniq_name

def chooseItem(game, level, location):
    items = loadItems(game, level, location)
    options = [item['name'] for item in items]
    choice = txt.getOption('Choose an item', options)
    return options[choice]

def chooseStartingLocation(game, level):
    prompt = "Choose a Starting Location"
    existing_locations = getLocations(game, level)
    options = existing_locations + ['A Container']
    choice = txt.getOption(prompt, existing_locations)
    if choice < len(existing_locations):
       starting_loc = existing_locations[choice]
    else:
        containers = getContainers(game, level)
        prompt = "Choose a Container"
        options = [txtUtil.properNoun(container.replace('_', '  '))
                                        for container in containers]
        choice = txt.getOption(prompt, options)
        starting_loc = containers[choice]
    formatted_loc = f"{getReference('locations', level, starting_loc)}.name"
    return formatted_loc

def chooseAnyLocation(game, allow_new_location = False):
    level = chooseLevel(game)
    prompt = "Choose Location"
    locations = getLocations(game, level)
    if allow_new_location:
        options = locations + ["New Location"]
    choice = txt.getOption(prompt, options)
    location = options[choice]
    if location == 'New Location':
        location = txt.getStr('Location Name (New)')
    return getReference('locations', level, location)

def chooseLocation(game, level, allow_new_location = False, exclude = []):
    prompt = "Choose a Location"
    options = getLocations(game, level)
    for exclusion in exclude:
        options.remove(exclusion)
    if allow_new_location:
        options.append('New Location')
    choice = txt.getOption(prompt, options)
    return options[choice]

def chooseConversation(game, level):
    prompt = "Choose a Conversation"
    existing_conversations = getConversations(game, level)
    options = existing_conversations
    choice = txt.getOption(prompt, existing_conversations)
    if choice < len(existing_conversations):
       conversation = existing_conversations[choice]
    formatted_convo = {
        'conversation': f"{getReference('conversations', level, conversation)}.conversation",
        'initial_msg': f"{getReference('conversations', level, conversation)}.initial_msg",
    }
    return formatted_convo

def chooseCharacter(game, level, location):
    prompt = "Choose a Character"
    character_names = getCharacters(game, level)
    characters = [loadConfig('characters', game, level, char_name) for char_name in character_names]
    char_objs =filter(lambda char: extractReference(char['start_location'])['obj_name'] == location, characters)
    options = [char_obj['name'] for char_obj in char_objs]
    choice = txt.getOption(prompt, options)
    return options[choice]

def getReference(obj_type, level, obj_name):
    return f"<{level}.{obj_type}.{obj_name.lower().replace(' ', '_')}>"

def getLocalizedReference(obj_type, level, location, obj_name):
    obj_name = obj_name.lower().replace(' ', '_')
    location = location.lower().replace(' ', '_')
    return f"<{level}.{obj_type}.{location}-{obj_name}>"

