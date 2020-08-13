nowhere_to_go = "*There's nowhere to go! I think I'm stuck...*"

malformed_take_request = "*I don't know what you want me to take.*"

malformed_talk_request = "*You want me to talk to who?*"

malformed_drop_request = "*I don't know what you want me to drop.*"

malformed_move_request = "*I don't understand where you want me to go.*"

malformed_talk_request = "*I don't understand who you want me to talk to.*"

empty_convo_selection = "Invalid selection"

def missingObj(obj_name):
    return f"*Hmm... Nope, I don't see any* @{obj_name}@ *here.*"

def missingContainer(item_name, container_name):
    return f"*I can't find a* @{container_name} *to take* @{item_name}@ *from!*"

def missingItem(item_name, container_name):
    return f"*Hmm... There's no* @{item_name}@ *in* {container_name}*.*"

def itemNotInInventory(item_name):
    return f"*I don't have a* @{item_name}@ *in my inventory.*"

def takingTakenItem(item_name):
    return f"*Err... and put it where exactly? If you want to* drop @{item_name}@*... well that's always an option.*"

def taken(item_name):
    return f"@{item_name}@ added to inventory."

def dropped(item_name):
    return f"@{item_name}@ dropped."

def untakeable(item_name):
    return f"*I don't think I can take* @{item_name}@*.*"

def defaultPathBlocked(path):
    return f"*The way to* ^{path}^ *is blocked.*"

def pathName(path):
    if path in ['north', 'south', 'east', 'west']:
        return f"*to the* ^{path}^"
    elif path in ['up', 'down']:
        return f"^{path}^"
    else:
        return f"*to* ^{path}^"

def invalidPath(path):
    return f"*I can't find a way* ^{pathName(path)}^*.*"

def characterNotFound(character_name):
    return f"*I don't see* {character_name} *here*"

def characterNotHere(character_name):
    return f"{character_name} *isn't here*"

