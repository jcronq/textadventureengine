import yaml

def printCommand(game, args):
    target = args.get('target', None)
    if target is None or target == 'state':
        print(yaml.dump(game.stateManager.state))

    if target == 'connections':
        cur_loc = game.getPlayerLocation()
        for key, con_obj in cur_loc.connections.items():
            print(f'{key}:')
            print(con_obj)

    if target == 'locations':
        for loc in game.locations.keys():
            print(loc)

