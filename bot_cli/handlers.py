from typing import Dict
from constants import Color, COMMAND_DESCRIPTIONS
from decorators import (
    handle_input_error,
    check_contact_exists,
    ensure_two_args,
    ensure_valid_phone_number,
    ensure_contacts_available,
    check_contact_existence,
)


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
