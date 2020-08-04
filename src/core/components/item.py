class Item:
    def __init__(self, uniq_name, name, description, start_location,
                 examine_text=None, takeable=True, take_text=None,
                 is_container=False, drop_text=None):
        self.uniq_name = uniq_name
        self.name = name
        self.description = description
        self.start_location = start_location
        self.examine_text = examine_text
        self.takeable = takeable
        self.take_text = take_text
        self.is_container = is_container
        self.drop_text = drop_text
        self.commands = {}

    def get_commands(self):
        self.commands

    def add_command(self, command_word, function, arguments, preconditions={}):
        self.commands[command_word] = (function, arguments, preconditions)

    def describe(self):
        container_txt = " - (container)" if self.is_container else ""
        return f"*{self.name}{container_txt}:*{self.description}"

    def examine(self):
        if self.examine_text is not None:
            return f"{self.examine_text}"
        else:
            return self.describe()

