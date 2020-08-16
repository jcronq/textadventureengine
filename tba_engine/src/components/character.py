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
        self.dialogue_tree = dialogue['conversation']
        self.initial_msg = dialogue['initial_msg']

    def converse(self, conversation_ref, selection):
        if conversation_ref == 'init':
            msg_ref = self.initial_msg
            opt_ref = self.dialogue_tree[msg_ref]['next']
        else:
            opt_ref = self.dialogue_tree[conversation_ref]['next']
            msg_ref = self.dialogue_tree[opt_ref]['opt'][selection]['next']
            opt_ref = self.dialogue_tree[msg_ref]['next']

        return {
            'npc_msg': self.dialogue_tree[msg_ref],
            'opts': self.dialogue_tree[opt_ref],
            'ref': msg_ref,
            'end': True if len(self.dialogue_tree[opt_ref]['opt']) == 0 else False
        }

