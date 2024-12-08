from constants import Color, Command
from utils import parse_input
from decorators import command_error_handler
from handlers import add_contact, change_contact, show_phone, show_all, show_help


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
