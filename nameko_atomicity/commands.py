from collections import UserDict, namedtuple
from typing import Union

from .exceptions import InvalidCommand

Command = namedtuple("Command", "func, args, kwargs")
""" Define a command class that must contain three parameters: func, args, kwargs """


def identify(obj):
    """Get the object id of string type"""

    return str(id(obj))


class DefaultListDict(UserDict):
    """Customize the dictionary with default value [],
    the value type of the dictionary is list.
    """

    def __missing__(self, key):
        """Default [] is returned in case of missing key"""

        self[key] = value = self.__default_value__()
        return value

    def __setitem__(self, key, value):
        self.__validate__(value)
        self.data[key] = value

    def __getattr__(self, item):
        return self[item]

    @staticmethod
    def __validate__(value):
        if not isinstance(value, list):
            raise TypeError(f"Must be of type `list`, but now it is `{type(value)}`.")

    @staticmethod
    def __default_value__():
        return list()

    def add(self, key, value):
        self[key].append(value)

    def insert(self, key, value, index: int):
        self[key].insert(index, value)


class CommandsBase(DefaultListDict):
    """The base class of Commands"""

    def append_command(self, container, command: Command):
        identify_id = identify(container)
        self.validate(command)
        super().add(identify_id, command)

    def insert_command(self, container, command: Command, index: int):
        identify_id = identify(container)
        self.validate(command)
        super().insert(identify_id, command, index)

    @staticmethod
    def validate(command):
        if not isinstance(command, Command):
            raise TypeError(
                f"Must be an instance of `:Command:`, "
                f"but now it's `{command.__class__}`."
            )

    @staticmethod
    def _adapt_parameters(args, kwargs):
        args = tuple() if not args else args
        kwargs = dict() if not kwargs else kwargs
        return args, kwargs

    def append(
        self, container, func, args: Union[tuple, list] = None, kwargs: dict = None
    ) -> None:
        args, kwargs = self._adapt_parameters(args, kwargs)

        command = Command(func=func, args=args, kwargs=kwargs)
        self.append_command(container, command)

    def insert(
        self,
        container,
        index,
        func,
        args: Union[tuple, list] = None,
        kwargs: dict = None,
    ) -> None:
        args, kwargs = self._adapt_parameters(args, kwargs)

        command = Command(func=func, args=args, kwargs=kwargs)
        self.insert_command(container, command, index)

    def exec_commands(self, container) -> list:
        identify_id = identify(container)
        commands = self.pop(identify_id, [])
        for command in commands:
            try:
                command.func(*command.args, **command.kwargs)
            except Exception as e:
                raise InvalidCommand({"command": command, "error_message": e})

        return commands

    def clear_commands(self, container) -> None:
        identify_id = identify(container)
        self.pop(identify_id, [])
