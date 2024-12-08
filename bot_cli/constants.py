from colorama import Fore
from enum import Enum
from typing import Dict
from functools import wraps


class Command(Enum):
    ADD = "add"
    CHANGE = "change"
    PHONE = "phone"
    ALL = "all"
    HELLO = "hello"
    EXIT = "exit"
    CLOSE = "close"
    HELP = "help"


class Color(Enum):
    SUCCESS = Fore.GREEN
    ERROR = Fore.RED
    INFO = Fore.BLUE
    WARNING = Fore.YELLOW
    TITLE = Fore.MAGENTA
    HIGHLIGHT = Fore.CYAN
    DEFAULT = Fore.WHITE


COMMAND_DESCRIPTIONS: Dict[Command, str] = {
    Command.ADD: "Add a new contact. Usage: add <name> <phone>",
    Command.CHANGE: "Change an existing contact's phone number. Usage: change <name> <phone>",
    Command.PHONE: "Show the phone number of a contact. Usage: phone <name>",
    Command.ALL: "Show all contacts.",
    Command.HELLO: "Greet the assistant.",
    Command.EXIT: "Exit the assistant.",
    Command.CLOSE: "Exit the assistant.",
    Command.HELP: "Show all available commands.",
}
