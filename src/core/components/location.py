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

    def addConnection(self, direction, location,
                            travel_description={},
                            travel_blockade={}):
        if direction.lower() in self.connections:
            raise DuplicateConnectionException(self.uniq_name, direction)

        self.connections[direction.lower()] = location
        self.blockades[direction.lower()] = travel_blockade.get('to', None)
        self.travel_descriptions[direction.lower()] = travel_description.get('to',None)

        if direction in cardinal_map:
            location.addAdjacentLocation(cardinal_map[direction], self, {
                    'to':travel_description.get('from', None),
                    'from':travel_description.get('to', None)
                },{
                    'to':travel_blockade.get('from', None),
                    'from':travel_blockade.get('to', None)
            })

    def examine(self):
        locations = "<br>- ".join(["Locations:"]+list(self.connections.keys()))
        return "*"+"<br><br>".join([self.name, self.description, locations])+"*"

