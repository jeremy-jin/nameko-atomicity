from functools import wraps

from nameko.extensions import DependencyProvider

from .commands import CommandsBase
from .dependency_base import CommandsWrapper


class _DispatchCommands(CommandsBase):
    pass


class DispatchCommands(DependencyProvider):

    """Dependency provider to access to the `::DispatchCommands::`.

    It will return a ``DispatchCommandsWrapper`` instance.
    """

    def get_dependency(self, worker_ctx):
        return CommandsWrapper(worker_ctx, _DispatchCommands)


def dispatch_after_commit(func):
    """Execute the dispatch event when the function call succeeds

    The following example demonstrates the use of::

        >>> from nameko.rpc import rpc
        >>> from nameko.events import EventDispatcher
        >>> from nameko_atomicity import DispatchCommands
        ...
        >>> class ConversionService(object):
        ...    name = "conversions"
        ...    event_dispatcher = EventDispatcher()
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

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            response = func(self, *args, **kwargs)
            self.dispatch_commands.exec_commands()
            return response
        except Exception as exc:
            raise exc

        finally:
            self.dispatch_commands.clear_commands()

    return wrapper
