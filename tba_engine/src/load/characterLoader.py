from src.components.character import Character

def characterLoader(character):
    name           = character['name']
    uniq_name      = character['uniq_name']
    description    = character['description']
    start_location = character['start_location']
    dialogue       = character['dialogue']
    examine_text   = character.get('examine_text', None)
    takeable       = character.get('takeable',     True)
    take_text      = character.get('take_text',    None)
    is_container   = character.get('is_container', False)
    drop_text      = character.get('drop_text',    None)

    character_obj = Character(name, description, start_location, examine_text,
        dialogue, takeable, take_text, is_container, drop_text)

    return character_obj

