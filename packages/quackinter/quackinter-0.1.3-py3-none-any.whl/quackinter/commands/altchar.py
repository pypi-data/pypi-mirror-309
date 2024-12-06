from quackinter.commands.command import Command
from quackinter.errors import InvalidArgError
from quackinter.key_injector import KeyInjector
from quackinter.stack import Stack


class AltCharCommand(Command):
    names = ["ALTCHAR", "ALT_CHAR"]

    def execute(self, stack: Stack, cmd: str, data: str) -> None:
        clean_data = data.strip()

        if len(clean_data) != 4 or not clean_data.isdigit():
            raise InvalidArgError(
                "Argument must be exactly four numbers for an alt code"
            )

        key_injector = KeyInjector(stack.environment)
        # with key_injector.hold("alt"):
        key_injector.key_down("alt")
        for num in clean_data:
            key_injector.press(f"num{num}")
        key_injector.key_up("alt")
