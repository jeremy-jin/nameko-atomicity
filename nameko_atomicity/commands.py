from collections import namedtuple, UserList
from typing import Union

from .exceptions import InvalidCommand

Command = namedtuple("Command", "func, args, kwargs")
""" Define a command class that must contain three parameters: func, args, kwargs """


class Commands(UserList):
    """The base class of Commands"""

    def append_command(self, command: Command):
        self.validate(command)
        super(Commands, self).append(command)

    def insert_command(self, index: int, command: Command):
        self.validate(command)
        super(Commands, self).insert(index, command)

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
        self, func, args: Union[tuple, list] = None, kwargs: dict = None
    ) -> None:
        args, kwargs = self._adapt_parameters(args, kwargs)

        command = Command(func=func, args=args, kwargs=kwargs)
        self.append_command(command)

    def insert(
        self,
        index,
        func,
        args: Union[tuple, list] = None,
        kwargs: dict = None,
    ) -> None:
        args, kwargs = self._adapt_parameters(args, kwargs)

        command = Command(func=func, args=args, kwargs=kwargs)
        self.insert_command(index, command)

    def exec_commands(self) -> list:
        commands = self.copy()
        self.clear()

        for command in commands:
            try:
                command.func(*command.args, **command.kwargs)
            except Exception as e:
                raise InvalidCommand({"command": command, "error_message": e})

        return list(commands)

    def clear_commands(self) -> None:
        self.clear()


class CommandsWrapper(object):
    def __init__(self, worker_ctx, commands_cls=Commands):
        self.worker_ctx = worker_ctx
        self._commands = commands_cls()

    def append_command(self, command: Command):
        self._commands.append_command(command)

    def insert_command(self, index: int, command: Command):
        self._commands.insert_command(index, command)

    def append(
        self, func, args: Union[tuple, list] = None, kwargs: dict = None
    ) -> None:
        self._commands.append(func, args, kwargs)

    def insert(
        self,
        index,
        func,
        args: Union[tuple, list] = None,
        kwargs: dict = None,
    ) -> None:
        self._commands.insert(index, func, args, kwargs)

    def exec_commands(self) -> list:
        return self._commands.exec_commands()

    def clear_commands(self):
        return self._commands.clear_commands()


class CommandsProxy(object):
    def __init__(self, items):
        self._items = items

    def __getattr__(self, name):
        def spawning_method(*args, **kwargs):
            items = self._items

            def call(item):
                return getattr(item, name)(*args, **kwargs)

            if items:
                return list(map(call, self._items))

        return spawning_method
