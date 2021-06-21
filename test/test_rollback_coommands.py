from mock import Mock

from nameko_atomicity import rollback_once_failed
from nameko_atomicity.rollback_commands import _RollbackCommands


class TestRollbackCommands:
    def test_get_dependency(self, rollback_commands, container):
        worker_ctx = Mock()
        worker_ctx.container = container
        dependency = rollback_commands.get_dependency(worker_ctx)

        assert isinstance(dependency, _RollbackCommands)


class TestRollbackOnceFailed:
    def test_successful(self, worker_ctx, rollback_commands, func):
        decorated_func = rollback_once_failed(func)
        dependency = rollback_commands.get_dependency(worker_ctx)
        setattr(dependency.container, "rollback_commands", dependency)

        func.return_value = "success"
        return_value = decorated_func(dependency.container)

        assert func.called
        assert return_value == "success"

    # def test_once_failed(self, worker_ctx, rollback_commands, func):
    #     decorated_func = rollback_once_failed(func)
    #     func.side_effect = Exception("Boom!")
    #     rollback_command = Mock()
    #     dependency = rollback_commands.get_dependency(worker_ctx)
    #     setattr(dependency.container, "rollback_commands", dependency)
    #     dependency.append(func=rollback_command, args="test_dispatch", kwargs={})
    #
    #     pytest.raises(Exception, decorated_func, dependency.container)
    #
    #     assert func.called
    #     assert rollback_command.called
