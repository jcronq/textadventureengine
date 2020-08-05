import sys
import yaml
import os

import src.text.textIO as txt
import src.text.textUtils as txtUtil
import src.config.util as util

def createNewItem():
    game = util.chooseGame()
    level = util.chooseLevel(game)
    item_uniq_name = util.chooseUniqueName('items', game, level)
    item_name = txt.getStr("Name", prompt_end = ":", default=item_uniq_name)
    start_location = util.chooseStartingLocation(game, level)
    description = txt.getStr("Description", prompt_end = ":")
    examine_text = txt.getStr("Examine Text", prompt_end = ":")
    is_container = txt.getYesNo("Is a container?\n> ")
    is_takeable = txt.getYesNo("Is takeable?\n> ")
    if is_takeable:
        take_text = txt.getStr("Take Text", prompt_end = ":")
        drop_text = txt.getStr("Drop Text", prompt_end = ":")
    else:
        take_text = None
        drop_text = None

    item_obj = {
        'name': item_name,
        'description': description,
        'start_location': start_location,
        'examine_text': examine_text,
        'takeable': is_takeable,
        'take_text': take_text,
        'drop_text': drop_text,
        'is_container': is_container
    }
    item_obj_defn = {
        item_uniq_name: item_obj
    }
    good = False
    while not good:
        print(yaml.dump(item_obj_defn))
        good = txt.getYesNo("Is this OK?\n> ")
        if not good:
            prompt = "What would you like to edit?"
            options = ["Unique Item Name"] + list(item_obj.keys())
            options.append("Nevermind, these are ok.")
            choice = txt.getOption(prompt, options)

            if choice == len(options)-1:
                good = True
            elif choice == 0:
                item_uniq_name = util.chooseUniqueName('items', game, level)
            else:
                key = options[choice]
                if key == 'takeable':
                    is_takeable = txt.getYesNo("Is takeable?\n> ")
                    if is_takeable and not item_obj_defn[item_uniq_name][key]:
                        item_obj['take_text'] = txt.getStr("Take Text")
                        item_obj['drop_text'] = txt.getStr("Drop )ext")
                    elif not is_takeable:
                        item_obj['take_text'] = None
                        item_obj['drop_text'] = None
                    item_obj[key] = is_takeable
                elif key == 'is_container':
                    item_obj[key] = txt.getYesNo("Is Container?\n> ")
                elif key == 'start_location':
                    item_obj[key] = util.chooseStartingLocation(game, level)
                else:
                    item_obj[key] = txt.getStr(key)

    save_file = util.getObjFileName('items', game, level, item_uniq_name)
    print(save_file)
    with open(save_file, 'w') as f:
        f.write("# This name MUST match the name of the file.\n")
        f.write(yaml.dump({'config': item_obj}))

createNewItem()

