from src.core.stateManager import StateManager

from functools import partial
import copy
import queue

PLAYER_LOCATION = 'player.location'
ITEM_ROOT = 'items'
LOCATION_ROOT = 'locations'
PLAYER_NAME = 'player.name'

obj_roots = {
    'item': ITEM_ROOT,
    'location': LOCATION_ROOT,
}

def itemInLocation(game, test_location, item):
    location = game.getItemLocation(item.name)
    return test_location.lower() in location.lower()

class Game:
    stateManager = StateManager()
    locations = {}
    items = {}
    text_buffer = queue.Queue()

    def __init__(self, start_location, locations, items):
        for location in locations:
            self.locations[location.name.lower()] = location
        for item in items:
            self.items[item.name.lower()] = item
            self.setItemLocation(item.name, item.start_location)
        self.setPlayerLocation(start_location)

    def getText(self):
        result = []
        while not self.text_buffer.empty() > 0:
            result.append(self.text_buffer.get())
        return result

    def report(self, reportable):
        if reportable is None:
            return
        if isinstance(reportable, str):
            self.text_buffer.put(reportable)
        elif isinstance(reportable, list):
            for txt in reportable:
                if isinstance(txt, str):
                    self.text_buffer.put(txt)
                else:
                    raise Exception()
        else:
            raise Exception()

    def load(self, state):
        self.stateManager.overrideStates(state)

    def getState(self, location, default=None):
        return self.stateManager.getState(location, default)

    def setState(self, location, value):
        self.stateManager.setState(location, value)

    def inConversation(self):
        state = 'player.is_conversing'
        return self.getState(state, False)

    def getInventoryContents(self):
        player_name = self.getState(PLAYER_NAME)
        filter_func = partial(itemInLocation, self, f'inventory.{player_name}')
        if len(self.items) <= 0:
            return []
        return list(filter(filter_func, self.items.values()))

    def getRoomContents(self):
        room_name = self.getPlayerLocation().name
        filter_func = partial(itemInLocation, self, room_name)
        if len(self.locations) <= 0:
            return []
        return list(filter(filter_func, self.items.values()))

    def getBlockerClearStatus(self, loc_name, path):
        root = self.getObjectRoot('item')
        state = f'{root}.{loc_name}.connections.{path}.block_cleared'
        self.getState(state, False)

    def setBlockerClearStatus(self, loc_name, path):
        root = self.getObjectRoot('item')
        state = f'{root}.{loc_name}.connections.{path}.block_cleared'
        self.setState(state, True)

    def getPlayerLocation(self):
        """Returns the Location() object of current room"""
        player_location_name = self.getState(PLAYER_LOCATION)
        return self.getLocation(player_location_name)

    def setPlayerLocation(self, new_location):
        self.setState(f"location.{new_location}.visited", True)
        self.setState(PLAYER_LOCATION, new_location)

    def getLocation(self, location_name, default=None):
        """Returns the Location() object associated with location_name"""
        return self.locations.get(location_name.lower(), default)

    def getItem(self, item_name, default=None):
        return self.items.get(item_name.lower(), default)

    def getItemsInLocation(self, test_location):
        filter_func = partial(itemInLocation, self, test_location)
        if len(self.items) <= 0:
            return []
        return list(filter(filter_func, self.items.values()))

    def getObjectRoot(self, obj_type):
        obj_root = obj_roots.get(obj_type, None)
        if obj_root is None:
            self.report(f"obj_type {obj_root} is missing its state root defined in game.py")
        return obj_root

    def getStateName_ItemLocation(self, item_name):
        return f'{ITEM_ROOT}.{item_name}.location'

    def getItemLocation(self, item_name):
        state_name = self.getStateName_ItemLocation(item_name.lower())
        return self.stateManager.getState(state_name, None)

    def setItemLocation(self, item_name, location):
        state_name = self.getStateName_ItemLocation(item_name.lower())
        self.stateManager.setState(state_name, location)

    def setExamined(self, obj_name, obj_type):
        obj_root = self.getObjectRoot(obj_type)

        state_name = f'{obj_root}.{obj_name}.examined'
        self.stateManager.setState(state_name, True)

    def getExamined(self, obj_name, obj_type):
        obj_root = getObjectRoot(obj_type)

        state_name = f'{obj_root}.{obj_name}.examined'
        return self.stateManager.getState(state_name, False)

    def hasItem(self, item_name):
        return item_name.lower() in self.items

    def addToInventory(self, item_name):
        location_state_name = self.getStateName_ItemLocation(item_name)
        player_name = self.getState(PLAYER_NAME)
        self.stateManager.setState(
            location_state_name,
            f'inventory.{player_name}'
        )

    def dropItem(self, item_to_drop):
        current_room = self.getState(PLAYER_LOCATION)
        location_state_name = self.getStateName_ItemLocation(item_to_drop)
        self.stateManager.setState(location_state_name, current_room)

    def getCharacter(self, character_name):
        return self.items.get(character_name.lower(), None)

    def getFullState(self):
        return copy.deepcopy(self.stateManager.state)

