import src.text.messages as messageTxt

import src.text.describe as describe

def converse(game, args):
    character = args.get('character', None)
    selection = args.get('selection', None)



    if character is None and selection is None:
        game.report(messageTxt.malformed_talk_request)

    if not game.inConversation():
        # Character not specified
        if character is None:
            game.report(messageTxt.malformed_talk_request)
            return
        else:
            char_obj = game.getCharacter(character)
            if char_obj == None:
                game.report(messageTxt.characterNotFound(character))
                return

            char_location = game.getCharacterLocation(character)
            player_location = game.getPlayerLocation().name
            if char_location != player_location:
                game.report(messageTxt.characterNotHere(character))
                return

            # Start conversation
            game.setInConversation(True)
            conv_obj = char_obj.converse('init', 0)

    # In conversation already
    else:
        # no response selected
        if selection is None:
            game.report(messageTxt.empty_convo_selection)
            return
        if not selection.isnumeric() or "." in selection:
            game.report(messageTxt.non_numeric_selection)
            return

        char_obj = game.getCharacter(character)
        conv_obj = char_obj.converse(game.getConversationRef(), int(selection))

    game.setConversationRef(character, conv_obj['ref'])
    game.report(
        describe.conversationMessage(
            character,
            conv_obj['npc_msg']['txt'],
            conv_obj['opts']['opt'],
        )
    )
    if conv_obj['end']:
        game.setInConversation(False)

