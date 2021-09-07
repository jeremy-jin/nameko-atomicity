import pytest

from nameko_atomicity.exceptions import InvalidCommand
from nameko_atomicity.commands import (
    CommandsWrapper,
    Command,
    Commands,
)


class Container(object):
    pass


class WorkerCtx:
    container = Container()


def func(*args, **kwargs):
    pass


class TestCommands:
    def func(*args, **kwargs):
        pass

    def func1(*args, **kwargs):
        raise TypeError("Error")

    class Container(object):
        pass

    commands = Commands()

    def test_append_command(self):
        self.commands.clear()
        command = Command(func=self.func, args=(), kwargs={})
        self.commands.append_command(command)
        assert self.commands
        assert len(self.commands) == 1
        assert self.commands[0] is command

    def test_append_command_with_type_error(self):
        pytest.raises(TypeError, self.commands.append_command, {})

    def test_insert_command(self):
        self.commands.clear()
        command = Command(func=self.func, args=(), kwargs={})
        command1 = Command(func=self.func, args=(), kwargs={})
        self.commands.insert_command(1, command)
        self.commands.insert_command(0, command1)

        assert self.commands
        assert len(self.commands) == 2
        assert self.commands[0] is command1
        assert self.commands[1] is command

    def test_append(self):
        self.commands.clear()
        self.commands.append(self.func)

        assert self.commands
        assert len(self.commands) == 1

    def test_insert(self):
        self.commands.clear()
        self.commands.insert(0, self.func)

        assert self.commands
        assert len(self.commands) == 1

    def test_exec_commands(self):
        self.commands.clear()
        self.commands.append(self.func)
        commands = self.commands.exec_commands()

        assert commands
        assert len(commands) == 1
        assert self.commands == []

    def test_exec_commands_with_invalid_command_error(self):
        self.commands.clear()
        self.commands.append(self.func1)
        pytest.raises(InvalidCommand, self.commands.exec_commands)

    def test_clear_commands(self):
        self.commands.clear()
        self.commands.append(self.func)

        assert self.commands
        assert len(self.commands) == 1

        self.commands.clear_commands()

        assert self.commands == []


class TestCommandsWrapper:
    worker_ctx = WorkerCtx()
    command_wrapper = CommandsWrapper(worker_ctx)
    command = Command(func=func, args=(), kwargs={})

    def test_add_command(self):
        self.command_wrapper.append_command(self.command)
        assert self.command_wrapper._commands
        assert len(self.command_wrapper._commands) == 1
        self.command_wrapper.clear_commands()
        assert len(self.command_wrapper._commands) == 0

    def test_insert_command(self):
        self.command_wrapper.clear_commands()
        self.command_wrapper.insert_command(0, self.command)
        command1 = Command(func=func, args=(), kwargs={})
        self.command_wrapper.insert_command(0, command1)

        assert self.command_wrapper._commands
        assert len(self.command_wrapper._commands) == 2
        assert self.command_wrapper._commands[0] == command1

    def test_append(self):
        self.command_wrapper.clear_commands()
        self.command_wrapper.append(func)
        assert self.command_wrapper._commands
        assert len(self.command_wrapper._commands) == 1

    def test_insert(self):
        self.command_wrapper.clear_commands()
        self.command_wrapper.insert(0, func)
        assert self.command_wrapper._commands
        assert len(self.command_wrapper._commands) == 1

    def test_exec_commands(self):
        self.command_wrapper.clear_commands()
        self.command_wrapper.insert(0, func)
        commands = self.command_wrapper.exec_commands()
        assert commands
        assert len(commands) == 1
