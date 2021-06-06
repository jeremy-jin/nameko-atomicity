from nameko_atomicity.commands import CommandsBase, Command
from nameko_atomicity.dependency_base import CommandsWrapper


class Container(object):
    pass


class WorkerCtx:
    container = Container()


class CommandsCase(CommandsBase):
    pass


def func(*args, **kwargs):
    pass


class TestCommandsWrapper:
    worker_ctx = WorkerCtx()
    command_wrapper = CommandsWrapper(worker_ctx, CommandsCase)
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
