cardinal_map = {
    'north': 'south',
    'south': 'north',
    'east': 'west',
    'west': 'east',
    'up': 'down',
    'down': 'up',
}

class DuplicateConnectionException(Exception):
    def __init__(location_name, direction):
        self.location  = location_name
        self.direction = direction

class Location:
    def __init__(self, uniq_name, name, description):
        self.uniq_name = uniq_name
        self.name = name
        self.description = description
        self.connections = {}
        self.travel_descriptions = {}
        self.blockades = {}
        self.examine_text = None

    def addConnection(self, direction, location_name,
                            travel_description,
                            travel_blockade={}):
        if direction.lower() in self.connections:
            raise DuplicateConnectionException(self.uniq_name, direction)

        self.connections[direction.lower()] = location_name
        if travel_blockade is not None:
            self.blockades[direction.lower()] = travel_blockade.get('to', None)
        self.travel_descriptions[direction.lower()] = travel_description

    def hasPath(self, path):
        return path.lower() in self.connections.keys()

    def examine(self):
        locations = "<br>- ".join(["Locations:"]+list(self.connections.keys()))
        return "*"+"<br><br>".join([self.name, self.description, locations])+"*"

