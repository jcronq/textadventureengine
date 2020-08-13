import os
import yaml
import re
import copy
import json

from src.load.itemLoader import itemLoader
from src.load.locationLoader import locationLoader
from src.load.characterLoader import locationLoader
from src.load.connectionLoader import connectionLoader

from src.core.game import Game
import src.config.util as util

obj_loaders = {
    "items": itemLoader,
    "locations": locationLoader,
    "characters": characterLoader,
}

class GameLoader:
    def __init__(self, game_name):
        self.game = None
        self.loadGameConfigs(game_name)
        self.createGameObjects()
        self.loadGameMeta(game_name)

    def getGameObject(self):
        return Game(
            self.initial_conditions['start_location'],
            self.extractLocations(self.object_tree, self.initial_conditions),
            self.extractItems(self.object_tree, self.initial_conditions)
        )

    def loadGameConfigs(self, game):
        self.levels = util.getLevels(game)
        self.objects = {}
        for level in self.levels:
            self.objects[level] = {
                'items': util.getItems(game, level),
                'locations': util.getLocations(game, level),
                'characters': util.getCharacters(game, level),
            }

        self.configs = {}
        for level, obj_configs in self.objects.items():
            self.configs[level] = {}
            for obj_type, objs in obj_configs.items():
                self.configs[level][obj_type] = {}
                for obj_name in objs:
                    obj_cfg = util.loadConfig(obj_type, game, level, obj_name)
                    obj_cfg['uniq_name'] = obj_name
                    self.configs[level][obj_type][obj_name] = obj_cfg

    def createGameObjects(self):
        self.str_data = self.resolveRawConfigs(self.configs, self.configs)
        self.object_tree = self.buildGameObjects(self.str_data)
        self.obj_data = self.resolveObjConfigs(
            self.str_data, self.object_tree)
        self.connectLocations(self.obj_data)

    def extractLocations(self, object_tree, initial_conditions):
        return self.extractObjs(object_tree, initial_conditions, 'locations')

    def extractItems(self, object_tree, initial_conditions):
        return self.extractObjs(object_tree, initial_conditions, 'items')

    def extractObjs(self, object_tree, initial_conditions, d_type):
        loadables = initial_conditions.get('load', []) + ['common']
        types = []
        load_location_objs = []
        for loadable in loadables:
            load_location_objs.append(object_tree.get(loadable, {}).get(d_type, {}))

        for load_obj in load_location_objs:
            for _, obj in load_obj.items():
                types.append(obj)
        return types

    def loadGameMeta(self, game):
        game_meta = util.getGameMeta(game)
        raw_init_cond = game_meta['initial_condition']
        str_init_cond = self.resolveRawConfigs(raw_init_cond, self.str_data)
        obj_init_cond = self.resolveObjConfigs(str_init_cond, self.object_tree)
        self.initial_conditions = obj_init_cond

    def connectLocations(self, obj_resolved_data):
        locations_data = {}
        for level_name, level_data in obj_resolved_data.items():
            level_objs = self.object_tree[level_name]
            for location_name, location_data in level_data.get('locations', {}).items():
                # if location_name == 'the_cutlass':
                #     import pdb; pdb.set_trace()
                location_obj = level_objs['locations'][location_name]
                connectionLoader(
                    location_obj,
                    location_data.get('connections',{}),
                    level_name
                )

    def buildGameObjects(self, resolved_data):
        obj_tree = {}
        for level_name, level_data in resolved_data.items():
            obj_tree[level_name] = {}
            for obj_type, objects in level_data.items():
                obj_tree[level_name][obj_type] = {}
                obj_loader = obj_loaders[obj_type]
                for obj_name, obj_datum in objects.items():
                    obj_tree[level_name][obj_type][obj_name] = obj_loader(obj_datum)
        return obj_tree

    def resolveObjConfigs(self, resolved_raw_data, object_tree):
        obj_regex = re.compile(r'<(.+)>')
        return self.resolveDependencies(
            resolved_raw_data, object_tree, obj_regex)

    def resolveRawConfigs(self, resolved_raw_data, lookup_obj):
        raw_regex = re.compile(r'<(.+)>\.(.+)')
        self._resolve_was_required = True
        while self._resolve_was_required:
            self._resolve_was_required = False
            resolved_raw_data = self.resolveDependencies(
                resolved_raw_data, lookup_obj, raw_regex)
        return resolved_raw_data

    def resolveDependencies(self, obj, lookup_obj, regex):
        if isinstance(obj, dict):
            new_obj = {}
            for key, value in obj.items():
                new_obj[key] = self.resolveDependencies(value, lookup_obj, regex)
            return new_obj
        elif isinstance(obj, list):
            return [self.resolveDependencies(item, lookup_obj, regex) for item in obj]
        elif isinstance(obj, str):
            matches = regex.findall(obj)
            if len(matches) > 0:
                if isinstance(matches[0], tuple):
                    lookup = matches[0][0].split('.') + [matches[0][1]]
                else:
                    lookup = matches[0].split('.')
                self._resolve_was_required = True
                return self.getObjValue(lookup_obj, lookup)
            else:
                return obj
        else:
            return obj

    def getObjValue(self, obj, lookup):
        if lookup[0] in obj:
            if len(lookup) == 1:
                return obj[lookup[0]]
            else:
                return self.getObjValue(obj[lookup[0]], lookup[1:])
        else:
            return None


    def loadLevels(self):
        raw_data = {}
        levels = os.listdir(f'{self.game_root}')
        level_names = filter(lambda f: 'yaml' not in f, levels)
        for level_name in level_names:
            raw_data = self.loadLevel(raw_data, level_name)
        return raw_data

    def loadLevel(self, raw_data, level_name):
        raw_data[level_name] = {}
        level_dir = f'{self.game_root}/{level_name}'
        dir_content = os.listdir(level_dir)
        for d_dir in dir_content:
            [d_type, _] = d_dir.split('.')
            d_dir_files = f'{level_dir}/{d_dir}'
            raw_data = self.loadDataDir(raw_data, d_dir_files, level_name, d_type)
        return raw_data

    def loadDataDir(self, raw_data, d_dir, level_name, d_type):
        d_dir_content = os.listdir(d_dir)
        d_files = [f'{d_dir}/{d_file_name}' for d_file_name in d_dir_content]
        raw_data[level_name][d_type] = {}
        for d_file in d_files:
            raw_data = self.loadDataFile(raw_data, d_file, level_name, d_type)
        return raw_data

    def loadDataFile(self, raw_data, d_file, level_name, d_type):
        with open(d_file, 'r') as f:
            content = yaml.full_load(f.read())
            for d_name, d_value in content.items():
                raw_data[level_name][d_type][d_name] = d_value
            # if d_type not in raw_data[level_name]:
            #     raw_data[level_name][d_type] = [content]
            # else:
            #     raw_data[level_name][d_type] += [content]
        return raw_data

