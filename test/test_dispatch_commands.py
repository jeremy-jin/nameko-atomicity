import pytest

from nameko_atomicity.dispatch_commands import _DispatchCommands
from nameko_atomicity import dispatch_after_commit


class TestDispatchCommands:
    def test_get_dependency(self, dispatch_commands, worker_ctx):
        dependency = dispatch_commands.get_dependency(worker_ctx)
        assert isinstance(dependency, _DispatchCommands)


class TestDispatchAfterCommit:
    def test_successful(self, worker_ctx, dispatch_commands, func):

        @dispatch_after_commit
        def dispatch(*args, **kwargs):
            pass

        decorated_func = dispatch_after_commit(func)

        dependency = dispatch_commands.get_dependency(worker_ctx)
        setattr(dependency.container, "dispatch_commands", dependency)

        dependency.append(func=dispatch, args="test_dispatch", kwargs={})
        func.return_value = "success"
        return_value = decorated_func(dependency.container)

        assert func.called
        assert return_value == "success"

    def test_once_failed(self, worker_ctx, dispatch_commands, func):
        decorated_func = dispatch_after_commit(func)
        dependency = dispatch_commands.get_dependency(worker_ctx)
        setattr(dependency.container, "dispatch_commands", dependency)
        func.side_effect = Exception("Boom!")
        pytest.raises(Exception, decorated_func, dependency.container)

        assert func.called
