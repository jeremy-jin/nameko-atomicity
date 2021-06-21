import pytest

from nameko_atomicity.exceptions import InvalidCommand
from nameko_atomicity.commands import (
    DefaultListDict, CommandsWrapper, Command, Commands, identify
)


class Container(object):
    pass


class WorkerCtx:
    container = Container()


def func(*args, **kwargs):
    pass


class TestDefaultListDict:
    def test_default_list_dict(self):
        default_dict = DefaultListDict()
        assert default_dict["name"] == []
        assert default_dict.name == []

        default_dict["name"] = ["p"]
        assert default_dict.name == ["p"]

        pytest.raises(TypeError, default_dict.__setitem__, "name", {})

        default_dict.add("name", "s")
        assert default_dict.name == ["p", "s"]

        default_dict.insert("case_insert", "done", 1)
        assert default_dict.case_insert == ["done"]
        default_dict.insert("case_insert", "done1", 0)
        assert default_dict.case_insert == ["done1", "done"]


class TestCommands:
    def func(*args, **kwargs):
        pass

    def func1(*args, **kwargs):
        raise TypeError("Error")

    class Container(object):
        pass

    commands = Commands()
    container = Container()

    def test_append_command(self):
        command = Command(func=self.func, args=(), kwargs={})
        self.commands.append_command(self.container, command)
        identify_id = identify(self.container)
        existing_commands = self.commands.pop(identify_id, [])
        assert existing_commands
        assert len(existing_commands) == 1
        assert existing_commands[0] is command

    def test_append_command_with_type_error(self):
        pytest.raises(TypeError, self.commands.append_command, self.container, {})

    def test_insert_command(self):
        command = Command(func=self.func, args=(), kwargs={})
        command1 = Command(func=self.func, args=(), kwargs={})
        self.commands.insert_command(self.container, command, 1)
        self.commands.insert_command(self.container, command1, 0)

        identify_id = identify(self.container)
        existing_commands = self.commands.pop(identify_id, [])

        assert existing_commands
        assert len(existing_commands) == 2
        assert existing_commands[0] is command1
        assert existing_commands[1] is command

    def test_append(self):
        self.commands.append(self.container, self.func)
        identify_id = identify(self.container)
        existing_commands = self.commands.pop(identify_id, [])

        assert existing_commands
        assert len(existing_commands) == 1

    def test_insert(self):
        self.commands.insert(self.container, 0, self.func)
        identify_id = identify(self.container)
        existing_commands = self.commands.pop(identify_id, [])

        assert existing_commands
        assert len(existing_commands) == 1

    def test_exec_commands(self):
        self.commands.append(self.container, self.func)
        commands = self.commands.exec_commands(self.container)

        assert commands
        assert len(commands) == 1

        identify_id = identify(self.container)
        existing_commands = self.commands.pop(identify_id, [])
        assert existing_commands == []

    def test_exec_commands_with_invalid_command_error(self):
        self.commands.append(self.container, self.func1)
        pytest.raises(InvalidCommand, self.commands.exec_commands, self.container)

    def test_clear_commands(self):
        self.commands.append(self.container, self.func)
        self.commands.clear_commands(self.container)
        identify_id = identify(self.container)
        commands = self.commands.pop(identify_id)
        assert commands == []


class TestCommandsWrapper:
    worker_ctx = WorkerCtx()
    command_wrapper = CommandsWrapper(worker_ctx)
    command = Command(func=func, args=(), kwargs={})

    def test_add_command(self):
        self.command_wrapper.append_command(self.command)
        commands = self.command_wrapper.clear_commands()
        assert commands
        assert len(commands) == 1

    def test_insert_command(self):
        self.command_wrapper.insert_command(self.command, 0)
        command1 = Command(func=func, args=(), kwargs={})
        self.command_wrapper.insert_command(command1, 0)
        commands = self.command_wrapper.clear_commands()
        assert commands
        assert len(commands) == 2
        assert commands[0] == command1

    def test_append(self):
        self.command_wrapper.append(func)
        commands = self.command_wrapper.clear_commands()
        assert commands
        assert len(commands) == 1

    def test_insert(self):
        self.command_wrapper.insert(0, func)
        commands = self.command_wrapper.clear_commands()
        assert commands
        assert len(commands) == 1

    def test_exec_commands(self):
        self.command_wrapper.insert(0, func)
        commands = self.command_wrapper.exec_commands()
        assert commands
        assert len(commands) == 1
