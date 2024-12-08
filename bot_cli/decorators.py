from functools import wraps
from typing import Callable, Any, List, Dict
from constants import Color


def ensure_two_args(func: Callable[[List[str]], str]) -> Callable[[List[str]], str]:
    @wraps(func)
    def handler(args: List[str], *other_args: Any, **kwargs: Any) -> str:
        if len(args) != 2:
            raise IndexError
        return func(args, *other_args, **kwargs)

    return handler


def handle_input_error(func: Callable[..., str]) -> Callable[..., str]:
    @wraps(func)
    def handler(*args: Any, **kwargs: Any) -> str:
        try:
            return func(*args, **kwargs)
        except KeyError:
            return f"{Color.ERROR.value}Error: Contact not found."
        except ValueError:
            return f"{Color.ERROR.value}Error: Error: Please provide both name and phone number."
        except IndexError:
            return f"{Color.ERROR.value}Error: Not enough arguments provided. Two arguments (name and phone) are required."

    return handler


def check_contact_exists(
    func: Callable[[List[str], Dict[str, str]], str]
) -> Callable[[List[str], Dict[str, str]], str]:
    @wraps(func)
    def handler(args: List[str], contacts: Dict[str, str]) -> str:
        name = args[0]
        if name not in contacts:
            return f"{Color.ERROR.value}Error: Contact '{name}' not found."
        return func(args, contacts)

    return handler


def ensure_contacts_available(
    func: Callable[[Dict[str, str]], str]
) -> Callable[[Dict[str, str]], str]:
    @wraps(func)
    def handler(contacts: Dict[str, str], *args: Any, **kwargs: Any) -> str:
        if not contacts:
            return f"{Color.WARNING.value}No contacts available."
        return func(contacts, *args, **kwargs)

    return handler


def check_contact_existence(
    func: Callable[[List[str], Dict[str, str]], str]
) -> Callable[[List[str], Dict[str, str]], str]:
    @wraps(func)
    def handler(args: List[str], contacts: Dict[str, str]) -> str:
        name = args[0]
        if name in contacts:
            return f"{Color.ERROR.value}Error: Contact '{name}' already exists."
        return func(args, contacts)

    return handler


def ensure_valid_phone_number(
    func: Callable[[List[str]], str]
) -> Callable[[List[str]], str]:
    @wraps(func)
    def handler(args: List[str], *other_args: Any, **kwargs: Any) -> str:
        _, phone = args
        if not phone.isdigit():
            raise ValueError(
                f"{Color.ERROR.value}Error: Invalid phone number. It must be numeric."
            )

        return func(args, *other_args, **kwargs)

    return handler


def command_error_handler(func: Callable[[str, Any], Any]) -> Callable[[str, Any], Any]:
    @wraps(func)
    def handler(command: str, *args: Any, **kwargs: Any) -> Any:
        try:
            return func(command, *args, **kwargs)
        except ValueError:
            print(
                f"{Color.ERROR.value}Error: Invalid command. Type 'help' to see available commands for the CLI."
            )
            return None

    return handler
