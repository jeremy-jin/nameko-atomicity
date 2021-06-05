from typing import Union

from commands import Command


class CommandsWrapper(object):
    def __init__(self, worker_ctx, commands_cls):
        self.worker_ctx, self.container = worker_ctx, worker_ctx.container
        self._rollback_commands = commands_cls()

    def add_command(self, command: Command):
        self._rollback_commands.add_command(self.container, command)

    def insert_command(self, command: Command, index: int):
        self._rollback_commands.insert_command(self.container, command, index)

    def append(
        self, func, args: Union[tuple, list] = None, kwargs: dict = None
    ) -> None:
        self._rollback_commands.append(self.container, func, args, kwargs)

    def insert(
        self,
        index,
        func,
        args: Union[tuple, list] = None,
        kwargs: dict = None,
    ) -> None:
        self._rollback_commands.insert(self.container, index, func, args, kwargs)

    def exec_commands(self) -> list:
        return self._rollback_commands.exec_commands(self.container)

    def clear_commands(self):
        return self._rollback_commands.clear_commands(self.container)
