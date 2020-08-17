from src.components.location import Location

def locationLoader(location_data):
    uniq_name      = location_data['uniq_name']
    name           = location_data['name']
    description    = location_data['description']
    connections     = location_data['connections']

    location = Location(uniq_name, name, description)

    for connection in connections:
        try:
            con_direction = connection['direction']
            location_name = connection.get('location')
            travel_blockade = connection.get('travel_blockade', {})
            travel_description = connection.get('travel_description', None)
            location.addConnection(con_direction, location_name,
                                   travel_description, travel_blockade)
        except:
            print(f"{location.name}, {connections}")
            raise Exception(f"'direction' not specified in {level_name}.{location.name}")

    return location

