def parsePrintArgs(command_parts):
    if len(command_parts) <= 0:
        return {'target':None}
    return {
        'target': " ".join(command_parts)
    }

def parseMoveArgs(command_parts):
    return {
        'location': " ".join(command_parts)
    }

def parseDropArgs(command_parts):
    return {
        'item': " ".join(command_parts)
    }

def parseConverseArgs(command_parts):
    if 'to' in command_parts:
        char = command_parts[command_parts.index('to')+1:]
    else:
        char = None

    return {
        'character': " ".join(char),
        'selection': " ".join(command_parts)
    }

def parseTakeArgs(command_parts):
    if 'from' in command_parts:
        itemName = " ".join(command_parts[0:command_parts.index('from')])
        container = " ".join(
            command_parts[command_parts.index('from')+1:len(command_parts)]
        )
    else:
        itemName = " ".join(command_parts) if len(command_parts) > 0 else None
        container = None
    return {
        'item': itemName,
        'from': container
    }

def parseExamineArgs(command_parts):
    if 'in' in command_parts:
        itemName = " ".join(command_parts[0:command_parts.index('in')])
        container = " ".join(
            command_parts[command_parts.index('in')+1:len(command_parts)]
        )
    else:
        itemName = " ".join(command_parts) if len(command_parts) > 0 else None
        container = None
    return {
        'item': itemName,
    }

class Parser:
    argument_parsers = {
        "move": parseMoveArgs,
        "examine": parseExamineArgs,
        "take": parseTakeArgs,
        "drop": parseDropArgs,
        "inventory": None,
        "use": None,
        "converse": parseConverseArgs,
        "sequence": None,
        "special": None,
        'print': parsePrintArgs,
    }

    def __init__(self):
        self.command_history = []

    def get_player_intent(self, command):
        command = command.lower()
        if "," in command:
            return "sequence"
        elif "move" in command or "go to " in command:
            return "move"
        elif "examine" in command or command.startswith("x "):
            return "examine"
        elif "take" in command or "get " in command:
            return "take"
        elif "drop " in command:
            return "drop"
        elif "inventory" in command or command == "i":
            return "inventory"
        elif "use " in command:
            return "use"
        elif "talk to " in command or "converse " in command:
            return "converse"
        elif ":quit" == command or ":q" == command:
            return "quit"
        elif ":print" in command or ":p" in command:
            return "print"
        else:
            #TODO: handle special commands
            return "special"

    def parse_command_args(self, intent, command):
        pass

    def parse_command(self, command):
        self.command_history.append(command)

        intent = self.get_player_intent(command)
        command_parts = command.split(" ")[1:]
        arg_parser = self.argument_parsers.get(intent, None)

        args = None
        if arg_parser is not None:
            args = arg_parser(command_parts)

        return {
            'intent': intent,
            'args':   args
        }

