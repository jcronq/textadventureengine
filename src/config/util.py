import sys
import yaml
import os

import src.text.textIO as txt
import src.text.textUtils as txtUtil

GAMES_ROOT = './games'

NONE_FILTER = lambda x: x is not None

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

def getObjFileName(obj_type, game, level, obj_name):
    file_name = f"{getObjRoot(obj_type, game, level)}/{obj_name.replace(' ','_')}.yaml"
    return file_name

def getGameMeta(game):
    meta_file_name = getMetaFile(game)
    print(meta_file_name)
    try:
        with open(meta_file_name, 'r') as f:
            contents = f.read()
            game_meta = yaml.full_load(contents)
            return game_meta
    except:
        return None

def loadConfig(obj_type, game, level, obj_name):
    normal_flat_name = obj_name.replace(' ', '_').lower()
    file_name = getObjFileName(obj_type, game, level, obj_name)
    try:
        with open(file_name, 'r') as f:
            content = f.read()
            obj = yaml.full_load(content)
            conf = obj['config']
            conf['uniq_name'] = obj_name
            return conf
    except:
        return None

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

def chooseGame():
    games = getGames()
    prompt = "Choose a game"
    options = [txtUtil.properNoun(game.replace('_', ' ')) for game in games]
    choice = txt.getOption(prompt, options)
    return games[choice]

def chooseLevel(game):
    levels = getLevels(game)
    prompt = "Choose Level"
    choice = txt.getOption(prompt, levels)
    return levels[choice]

def chooseUniqueName(obj_type, game, level):
    existing_objs = getGameObjects(obj_type, game, level)
    existing_names = [obj.replace('_', ' ').lower() for obj in existing_objs]
    item_uniq_name = txt.getStr("Unique Name")
    while item_uniq_name.lower().replace('_', ' ') in existing_names:
        item_uniq_name = txt.getStr(f"{item_uniq_name} is already taken. Please choose another\nUnique Name")
    return item_uniq_name

def chooseStartingLocation(game, level):
    prompt = "Choose a Starting Location"
    existing_locations = getLocations(game, level)
    options = existing_locations + ['A Container']
    choice = txt.getOption(prompt, existing_locations)
    if choice != len(existing_locations):
       starting_loc = existing_locations[choice]
    else:
        containers = getContainers(game, level)
        prompt = "Choose a Container"
        options = [txtUtil.properNoun(container.replace('_', '  '))
                                        for container in containers]
        choice = txt.getOption(prompt, options)
        starting_loc = containers[choice]
    formatted_loc = f"<{level}.locations.{starting_loc}>.name"
    return formatted_loc

