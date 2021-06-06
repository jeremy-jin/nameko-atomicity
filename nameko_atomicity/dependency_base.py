from typing import Union

from .commands import Command


class CommandsWrapper(object):
    def __init__(self, worker_ctx, commands_cls):
        self.worker_ctx, self.container = worker_ctx, worker_ctx.container
        self._commands = commands_cls()

    def append_command(self, command: Command):
        self._commands.append_command(self.container, command)

    def insert_command(self, command: Command, index: int):
        self._commands.insert_command(self.container, command, index)

    def append(
        self, func, args: Union[tuple, list] = None, kwargs: dict = None
    ) -> None:
        self._commands.append(self.container, func, args, kwargs)

    def insert(
        self,
        index,
        func,
        args: Union[tuple, list] = None,
        kwargs: dict = None,
    ) -> None:
        self._commands.insert(self.container, index, func, args, kwargs)

    def exec_commands(self) -> list:
        return self._commands.exec_commands(self.container)

    def clear_commands(self):
        return self._commands.clear_commands(self.container)
