def connectionLoader(location, connections, level_name):
    for connection in connections:
        try:
            con_direction = connection['direction']
        except:
            print(f"{location.name}, {connections}")
            raise Exception(f"'direction' not specified in {level_name}.{location.name}")
        try:
            con_location = connection['location']
        except:
            print(f"{location.name}, {connections}")
            raise Exception(f"'location' not specified in {level_name}.{location.name}")
        travel_blockade = connection.get('travel_blockade', {})
        travel_description = connection.get('travel_description', {})

        location.addConnection(con_direction, con_location,
            travel_description, travel_blockade)

    return location

