import src.text.messages as messageTxt
def converse(game, args):
    character = args.get('character', None)
    selection = args.get('selection', None)

    if character is None and selection is None:
        game.report(messageTxt.malformed_talk_request)

    conversation = game.getConversation(character)

    if not game.inConversation():
        game.setConversationRef('init')

    else:
        if selection is None:
            game.report(messageTxt.emptyConvoSelection)
        game.

    game.report(conversation.)

