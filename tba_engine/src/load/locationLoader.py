from src.components.location import Location

def locationLoader(location_data):
    uniq_name      = location_data['uniq_name']
    name           = location_data['name']
    description    = location_data['description']

    location = Location(uniq_name, name, description)

    return location

