from nameko_atomicity.dispatch_commands import _DispatchCommands


class TestDispatchCommands:
    def test_get_dependency(self, dispatch_commands, worker_ctx):
        dependency = dispatch_commands.get_dependency(worker_ctx)
        assert isinstance(dependency, _DispatchCommands)
