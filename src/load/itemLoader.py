from src.core.components.item import Item

def itemLoader(item):
    name           = item['name']
    uniq_name      = item['uniq_name']
    description    = item['description']
    start_location = item['start_location']
    examine_text   = item.get('examine_text', None)
    takeable       = item.get('takeable',     True)
    take_text      = item.get('take_text',    None)
    is_container   = item.get('is_container', False)
    drop_text      = item.get('drop_text',    None)

    item_obj = Item(uniq_name, name, description, start_location, examine_text,
        takeable, take_text, is_container, drop_text)

    return item_obj

