import inspect

import wrapt
from nameko.extensions import DependencyProvider

from .commands import CommandsWrapper, CommandsProxy


class _DispatchCommands(CommandsWrapper):
    pass


class DispatchCommandsDependencyProvider(DependencyProvider):

    """Dependency provider to access to the `::DispatchCommands::`.

    It will return a ``DispatchCommandsWrapper`` instance.
    """

    @classmethod
    def dispatch_after_commit(cls, wrapped=None, *args, **kwargs):
        """Execute the dispatch event when the function call succeeds

        The following example demonstrates the use of::

            >>> from nameko.rpc import rpc
            >>> from nameko.events import EventDispatcher
            >>> from nameko_atomicity import DispatchCommands
            ...
            >>> class ConversionService(object):
            ...    name = "conversions"
            ...    dispatch_commands = DispatchCommands()
            ...
            ...    @rpc
            ...    @dispatch_after_commit
            ...    def inches_to_cm(self, inches):
            ...        event_name = "booking_updated"
            ...        dispatch_data = {}
            ...        self.dispatch_commands.append(
            ...            func=self.event_dispatcher,
            ...            args=(event_name, dispatch_data),
            ...            kwargs={},
            ...        )

        """

        def find_commands_providers(instance):
            commands_provides = inspect.getmembers(
                instance, lambda obj: isinstance(obj, _DispatchCommands)
            )
            return commands_provides

        @wrapt.decorator
        def wrapper(wrapped, instance, args, kwargs):
            commands_provides = find_commands_providers(instance)
            commands_provides = [
                commands_provide[1] for commands_provide in commands_provides
            ]
            try:
                response = wrapped(*args, **kwargs)
                CommandsProxy(commands_provides).exec_commands()
                return response

            finally:
                CommandsProxy(commands_provides).clear_commands()

        if wrapped:
            return wrapper(wrapped)

        return wrapper

    def get_dependency(self, worker_ctx):
        return _DispatchCommands(worker_ctx)


DispatchCommands = DispatchCommandsDependencyProvider
dispatch_after_commit = DispatchCommandsDependencyProvider.dispatch_after_commit
