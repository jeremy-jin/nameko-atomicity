from mock import Mock

from nameko_atomicity.rollback_commands import _RollbackCommands


class TestRollbackCommands:
    def test_get_dependency(self, rollback_commands, container):
        worker_ctx = Mock()
        worker_ctx.container = container
        dependency = rollback_commands.get_dependency(worker_ctx)

        assert isinstance(dependency, _RollbackCommands)
