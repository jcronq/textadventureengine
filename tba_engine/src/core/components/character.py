from core.components.item import Item

class Character(Item):
    def __init__(self, name, description, examine_text, dialouge_tree, takeable=False,
                 take_text=None):
        super.__init__(name,
                       description,
                       examine_text,
                       takeable,
                       take_text,
                       is_container=True
                       )
        self.name = name
        self.description = description
        self.dialouge_tree = dialouge_tree

