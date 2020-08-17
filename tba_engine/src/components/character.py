from src.components.item import Item

class Character(Item):
    def __init__(self, name, description, start_location, examine_text,
                 dialogue, takeable=False, take_text=None,
                 drop_text=None, is_container=True):
        super().__init__(name, name,
                       description,
                       start_location,
                       examine_text=examine_text,
                       takeable=takeable,
                       take_text=take_text,
                       drop_text=drop_text,
                       is_container=is_container,
                       )
        self.dialogue_tree = {}
        self.initial_msg = {}
        for convo_conf in dialogue:
            loc = convo_conf['location']
            self.dialogue_tree[loc] = convo_conf['conversation']
            self.initial_msg[loc] = convo_conf['initial_msg']

    def isConversable(self, location):
        return location in self.dialogue_tree

    def converse(self, conversation_ref, selection, location):
        location = location.lower().replace(' ', '_')
        if conversation_ref == 'init':
            msg_ref = self.initial_msg[location]
            opt_ref = self.dialogue_tree[location][msg_ref]['next']
        else:
            opt_ref = self.dialogue_tree[location][conversation_ref]['next']
            msg_ref = self.dialogue_tree[location][opt_ref]['opt'][selection]['next']
            if msg_ref is None:
                return {
                    'npc_msg': None,
                    'opts': None,
                    'ref': None,
                    'end': True,
                }
            opt_ref = self.dialogue_tree[location][msg_ref]['next']

        return {
            'npc_msg': self.dialogue_tree[location][msg_ref],
            'opts': self.dialogue_tree[location][opt_ref],
            'ref': msg_ref,
            'end': True if len(self.dialogue_tree[location][opt_ref]['opt']) == 0 else False
        }

