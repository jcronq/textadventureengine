import src.text.messages as messages

def take(item_obj):
    if item_obj.take_text is not None:
        take_description = f"*{item_obj.take_text}*<br>"
    else:
        take_description = ""
    return take_description+messages.taken(item_obj.name)

def drop(item_obj):
    if item_obj.drop_text is not None:
        drop_description = f"*{item_obj.drop_text}*<br>"
    else:
        drop_description = ""
    return drop_description+messages.dropped(item_obj.name)

def blockedPath(path, blocker):
    if (blocker_text := blocker.get('txt', None)) is not None:
        return f"*{blocker_text}*"
    else:
        return messages.defaultPathBlocked(path)

def clearBlockade(blocker):
    if cleared_text := blocker.get('txt', None) is not None:
        return f"*{cleared_text}*"
    return cleared_text

def move(current_location, destination):
    travel_description = current_location.travel_descriptions.get(destination.lower(), None)
    return f"*{travel_description}*"

def item(item_obj):
    hints = []
    if item_obj.is_container:
        hints.append("container")
    if item_obj.takeable:
        hints.append("takeable")

    if len(hints) > 0:
        hint_text = f" - ({','.join(hints)})"
    else:
        hint_text = ""

    return f"@{item_obj.name}@: *{item_obj.description}*"

def location(loc_obj):
    if len(loc_obj.connections) > 0:
        adjacents_text = "<br>- ".join([f'^{loc}^' for loc in loc_obj.connections.keys()])
        connections_text = f"#Connected Locations#:<br>- {adjacents_text}"
    else:
        connections_text = messages.nowhere_to_go
    description = [
        f"^{loc_obj.name}^: *{loc_obj.description}*",
        connections_text
    ]
    return "<br><br>".join(description)

def inventory(inventory_contents):
    item_description = [item(item_obj) for item_obj in inventory_contents]
    return "#Inventory Contents#:<br>- "+"<br>- ".join(item_description)

