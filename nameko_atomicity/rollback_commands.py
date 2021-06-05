from functools import wraps

from nameko.extensions import DependencyProvider

from commands import CommandsBase, identify
from dependency_base import CommandsWrapper


class _RollbackCommands(CommandsBase):
    pass


class RollbackCommands(DependencyProvider):

    """Dependency provider to access to the `::RollbackCommands::`.

    It will return a ``RollbackCommandsWrapper`` instance.
    """

    def get_dependency(self, worker_ctx):
        return CommandsWrapper(worker_ctx, _RollbackCommands)


def rollback_once_failed(func):
    """Execute the rollback command when a function call fails

    The following example demonstrates the use of::

        >>> from nameko.rpc import rpc
        ... from nameko_atomicity import RollbackCommands
        ...
        ... def rollback_function():
        ...     pass
        ...
        ... class ConversionService(object):
        ...    name = "conversions"
        ...
        ...    rollback_commands = RollbackCommands()
        ...
        ...    @rpc
        ...    @rollback_once_failed
        ...    def inches_to_cm(self, inches):
        ...        self.rollback_commands.append(
        ...            func=rollback_function,
        ...            args=(),
        ...            kwargs={},
        ...        )

    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            response = func(self, *args, **kwargs)
        except Exception as exc:
            self.rollback_commands.exec_commands()
            raise exc

        finally:
            self.rollback_commands.clear_commands()

        return response

    return wrapper
