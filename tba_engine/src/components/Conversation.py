
conversationTypes = ['npc', 'player', 'player-opt']

class ConversationMessage:

    def __init__(self, message = None, _next = None, condition = None):
        self.condition = condition
        self.next = _next
        self.message = message

    def process(self, charName):
        return self.next

class PlayerMessage(ConversationMessage):
    type = 'player'

    def process(self, charName):
        return self.next

class NpcMessage(ConversationMessage):
    type = 'npc'

    def process(self, charName):
        self.next

class Conversation:
    def __init__(self, startRef):
        self.startRef = startRef
        self.messageMap = {}

    def addMessage(self, msgRef, message):
        self.messageMap[msgRef] = message

