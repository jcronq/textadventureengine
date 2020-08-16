import src.text.describe as describe

def enumerateItems(msg, items):
    item_descriptions = "<br>- ".join(list([
        describe.item(item) for item in items
    ]))
    return "<br>- ".join([
        msg,
        item_descriptions
    ])

def item(item, sub_items = []):
    item_txt = []
    if item.examine_text is not None:
        item_txt.append(f"*{item.examine_text}*")
    else:
        item_txt.append(describe.item(item))

    if len(sub_items) > 0:
        message = "*It looks like there there's something inside...*"
        container_description = enumerateItems(message, sub_items)
        item_txt.append(container_description);
    return "<br><br>".join(item_txt)

def location(loc, items = [], characters = []):
    location_txt = []
    if loc.examine_text is not None:
        location_txt.append(loc.examine_text)
    else:
        location_txt.append(describe.location(loc))

    if len(characters) > 0:
        message = "#Notable People#:"
        char_description = enumerateItems(message, characters)
    else:
        char_description = ""

    if len(items) > 0:
        message = "#Notable Objects#:"
        item_description = enumerateItems(message, items)
    elif len(characters) > 0:
        item_description = ""
    else:
        item_description = "*Nothing noteworthy here.*"

    if len(item_description) > 0:
        location_txt.append(item_description)
    if len(char_description) > 0:
        location_txt.append(char_description)
    return "<br><br>".join(location_txt)

