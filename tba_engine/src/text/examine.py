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

def location(loc, items = []):
    location_txt = []
    if loc.examine_text is not None:
        location_txt.append(loc.examine_text)
    else:
        location_txt.append(describe.location(loc))

    if len(items) > 0:
        message = "#Notable Objects#:"
        item_description = enumerateItems(message, items)
    else:
        item_description = "*Nothing noteworthy here.*"

    location_txt.append(item_description)
    return "<br><br>".join(location_txt)

