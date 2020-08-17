def connectionLoader(location, connections, level_name):
    for connection in connections:
        try:
            con_direction = connection['direction']
        except:
            print(f"{location.name}, {connections}")
            raise Exception(f"'direction' not specified in {level_name}.{location.name}")

        location_name = connection.get('location')
        travel_blockade = connection.get('travel_blockade', {})
        travel_description = connection.get('travel_description', None)

        location.addConnection(con_direction, location_name,
                               travel_description, travel_blockade)

    return location

