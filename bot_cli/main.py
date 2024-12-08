from colorama import Fore, init
from enum import Enum
from typing import Dict, Tuple, Any, Callable
from functools import wraps

init(autoreset=True)


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


def ensure_two_args(func: Callable) -> Callable:
    @wraps(func)
    def handler(args: list[str], *other_args, **kwargs) -> str:
        if len(args) != 2:
            raise IndexError
        return func(args, *other_args, **kwargs)

    return handler


def handle_input_error(func: Any):
    @wraps(func)
    def handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return f"{Color.ERROR.value}Error: Contact not found."
        except ValueError:
            return f"{Color.ERROR.value}Error: Error: Please provide both name and phone number."
        except IndexError:
            return f"{Color.ERROR.value}Error: Not enough arguments provided. Two arguments (name and phone) are required."

    return handler


def check_contact_exists(func: Callable) -> Callable:
    @wraps(func)
    def handler(args: list[str], contacts: Dict[str, str]) -> str:
        name = args[0]
        if name not in contacts:
            return f"{Color.ERROR.value}Error: Contact '{name}' not found."
        return func(args, contacts)

    return handler


def ensure_contacts_available(func: Callable) -> Callable:
    @wraps(func)
    def handler(contacts: Dict[str, str], *args, **kwargs) -> str:
        if not contacts:
            return f"{Color.WARNING.value}No contacts available."
        return func(contacts, *args, **kwargs)

    return handler


def check_contact_existence(func: Callable) -> Callable:
    @wraps(func)
    def handler(args: list[str], contacts: Dict[str, str]) -> str:
        name = args[0]
        if name in contacts:
            return f"{Color.ERROR.value}Error: Contact '{name}' already exists."
        return func(args, contacts)

    return handler


def ensure_valid_phone_number(func: Callable) -> Callable:
    @wraps(func)
    def handler(args: list[str], *other_args, **kwargs) -> str:
        _, phone = args
        if not phone.isdigit():
            return (
                f"{Color.ERROR.value}Error: Invalid phone number. It must be numeric."
            )
        return func(args, *other_args, **kwargs)

    return handler


def command_error_handler(func: Callable) -> Callable:
    @wraps(func)
    def handler(command: str, *args, **kwargs) -> Any:
        try:
            return func(command, *args, **kwargs)
        except ValueError:
            print(
                f"{Color.ERROR.value}Error: Invalid command. Type 'help' to see available commands for the CLI."
            )
            return None

    return handler


def parse_input(user_input: str) -> Tuple[str, list[str]]:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@handle_input_error
@check_contact_existence
@ensure_two_args
@ensure_valid_phone_number
def add_contact(args: list[str], contacts: Dict[str, str]) -> str:
    name, phone = args
    contacts[name] = phone
    return f"{Color.SUCCESS.value}Contact added."


@handle_input_error
@check_contact_exists
@ensure_two_args
@ensure_valid_phone_number
def change_contact(args: list[str], contacts: Dict[str, str]) -> str:
    name, phone = args
    contacts[name] = phone
    return f"{Color.SUCCESS.value}Contact changed."


@handle_input_error
@check_contact_exists
def show_phone(args: list[str], contacts: Dict[str, str]) -> str:
    (name,) = args
    phone = contacts.get(name)
    return f"{Color.INFO.value}{name}: {phone}"


@handle_input_error
@ensure_contacts_available
def show_all(contacts: Dict[str, str]) -> str:
    result = [f"{Color.HIGHLIGHT.value}All Contacts:"]
    for name, phone in contacts.items():
        result.append(f"{Color.INFO.value}{name}: {phone}")
    return "\n".join(result)


@handle_input_error
def show_help() -> str:
    result = [f"{Color.HIGHLIGHT.value}Available Commands:"]
    for command, description in COMMAND_DESCRIPTIONS.items():
        result.append(f"{Color.DEFAULT.value}{command.value}: {description}")
    return "\n".join(result)


@command_error_handler
def parse_command(command: str) -> Command:
    return Command(command)


def main() -> None:
    print(f"{Color.TITLE.value}Welcome to the assistant bot!")
    contacts = {}

    try:
        while True:
            user_input = (
                input(f"{Color.DEFAULT.value}Enter a command: ").strip().lower()
            )
            command, *args = parse_input(user_input)

            parsed_command = parse_command(command)

            if parsed_command is None:
                continue

            match parsed_command:
                case Command.EXIT | Command.CLOSE:
                    print(f"{Color.TITLE.value}Good bye!")
                    break
                case Command.HELLO:
                    print(f"{Color.TITLE.value}How can I help you?")
                case Command.ADD:
                    print(add_contact(args, contacts))
                case Command.CHANGE:
                    print(change_contact(args, contacts))
                case Command.PHONE:
                    print(show_phone(args, contacts))
                case Command.ALL:
                    print(show_all(contacts))
                case Command.HELP:
                    print(show_help())
                case _:
                    print(f"{Color.ERROR.value}Error: Invalid command.")
    except Exception as e:
        print(f"{Color.ERROR.value}Exeption: {e}")


if __name__ == "__main__":
    main()
