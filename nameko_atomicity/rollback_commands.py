import inspect

import wrapt
from nameko.extensions import DependencyProvider

from .commands import CommandsWrapper


class _RollbackCommands(CommandsWrapper):
    pass


class RollbackCommandsDependencyProvider(DependencyProvider):

    """Dependency provider to access to the `::RollbackCommands::`.

    It will return a ``RollbackCommandsWrapper`` instance.
    """

    @classmethod
    def rollback_once_failed(cls):
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

        def find_commands_providers(instance):
            commands_provides = inspect.getmembers(
                instance, lambda obj: isinstance(obj, _RollbackCommands)
            )
            return commands_provides

        @wrapt.decorator
        def wrapper(wrapped, instance, args, kwargs):
            commands_provides = find_commands_providers(instance)

            try:
                response = wrapped(instance, *args, **kwargs)
            except Exception as exc:
                for commands_provide in commands_provides:
                    commands_provide.exec_commands()

                raise exc

            finally:
                for commands_provide in commands_provides:
                    commands_provide.clear_commands()

            return response

        return wrapper

    def get_dependency(self, worker_ctx):
        return _RollbackCommands(worker_ctx)


RollbackCommands = RollbackCommandsDependencyProvider
rollback_once_failed = RollbackCommandsDependencyProvider.rollback_once_failed()
